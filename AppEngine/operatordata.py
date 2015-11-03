from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from gradientone import query_to_dict
from gradientone import convert_str_to_cha_list
from gradientone import get_ordered_list
from gradientone import co_and_tp_names
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000data
from onedb import agilentU2000_key
from onedb import TestInterface
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import CommentsDB
from onedb import TestDB
from onedb import StateDB
import itertools
import jinja2
import webapp2
import logging
import datetime
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
import json

# result_types = {
#     'bscope' : BscopeDB,
#     'aU2000' : agilentU2000data
# }

class Handler(InstrumentDataHandler):

    def get(self,company_nickname="", hardware_name="",config_name="",
        start_tse=""):
        "retrieve instrument data by instrument name and time start_tse"

        testplan_name = self.request.get('testplan')

        query = ConfigDB.all().filter("company_nickname =", company_nickname)
        query.filter("hardware_name =", hardware_name)
        query.filter("config_name =", config_name)
        config = query.get()
        # configkey = 'company_nickname'+'hardware_name'+'config_name'
        # config = memcache.get(configkey)

        if config is None:
            logging.error("ConfigData:get: query")
            config = '{"instrument_type": "sample inputs", "config_name": "config1", "company_nickname": "GradientOne", "trace_name": "trace1", "title": "T1"}'
        else:
            config = config.to_dict()
        templatedata = {
                'config': config,
                'company_nickname' : company_nickname,
                'hardware_name' : hardware_name,
                'config_name' : config_name,
                'start_tse' : start_tse,
                'testplan_name' : testplan_name,
                }

        # resultKey = BscopeDB_key(company_nickname, config_name)
        # result = BscopeDB.get(resultKey)

        query = TestDB.all().filter("company_nickname =", company_nickname)
        query = query.filter("testplan_name =", testplan_name)
        test = query.get()
        comment_thread = []
        if hasattr(test, 'comments'):
            for comment in test.comments:
                comment_thread.append(comment)

        templatedata['comment_thread'] = comment_thread
    
        # ToDo - check for results. If True, then show below.
        results = False
        if results:
            key = testplan_name + company_nickname + hardware_name + config_name + start_tse
            cached_copy = memcache.get(key)
            if cached_copy is None:

                result_data = TestResultsDB.all().get()
                data = result_data.to_dict()
                if not data:
                    logging.error("ResultData:get: query")
                    templatedata['results'] = "Error: No result data"
                    self.render('operator.html', data=templatedata)               
                # ToDo: Add handler to check data for bscope 
                bscope = False
                if bscope:
                    print data
                    cha_list = convert_str_to_cha_list(data['cha'])
                    data['cha'] = cha_list
                    e = data
                    print e
                    print type(e)
                    output = {"data":data}
                else:
                    # pull data for aU2000
                    e = data['test_results_data']
                output = json.dumps(e)
                memcache.set(key, output)
                templatedata['results'] = output
                self.render('operator.html', data=templatedata)
                #render_json_cached(self, output)
            else:
                templatedata['results'] = cached_copy
                self.render('operator.html', data=templatedata)
                #render_json_cached(self, cached_copy)
        else:
            self.render('operator.html', data=templatedata)

    def post(self, company_nickname="", hardware_name="",config_name="",
        start_tse=""):
        """posts a comment on the test results"""
        user = users.get_current_user()
        if not user.nickname():
            author = "anonymous"
        else:
            author = user.nickname()
        testplan_name = self.request.get('testplan')
        content = self.request.get('content')
        query = TestDB.all().filter("company_nickname =", company_nickname)
        query = query.filter("testplan_name =", testplan_name)
        test = query.get()
        comment = CommentsDB(author=author, content=content, test=test)
        comment.put()
        self.redirect('/operator/{0}/{1}/{2}/{3}?testplan={4}'.format(
            company_nickname, hardware_name, config_name, start_tse, testplan_name))


class RunTest(InstrumentDataHandler):
    def post(self, company_nickname="", hardware_name="",config_name="",
        start_tse=""):
        # company_nickname = self.request.get('company_nickname')
        # testplan_name = self.request.get('testplan')
        # names = (company_nickname,testplan_name)

        names = co_and_tp_names(self.request.body)
        results = db.GqlQuery("SELECT configs FROM TestDB WHERE company_nickname =:1 and testplan_name =:2",
            names[0], names[1])
        for r in results:
            config = db.get(r.configs[0])
            config_dict = {}
            config_dict['company_nickname'] = config.company_nickname
            config_dict['config_name'] = config.config_name
            config_dict['hardware_name'] = config.hardware_name
            config_dict['instrument_type'] = config.instrument_type
            config_dict['number_of_samples'] = config.number_of_samples
        results = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", names[0], names[-1])
        test_dict = [c.to_dict() for c in results]
        try:
            order = str(test_dict[0]['order'])
            print "order:"
            print order
            order_list = get_ordered_list(order)
            print "order_list:"
            print order_list
        except (IndexError, KeyError) as e:
            logging.error("Index-Key_Error: Order List")
            order_list = ""
        for o in order_list:
            op = StateDB(key_name = (names[-1]+o['type']+o['name']), parent = company_key(),
                    testplan_name = names[-1],
                    company_nickname = names[0],
                    widget = o['type'],
                    name = o['name'],
                    order = int(o['order']),
                    )
            op.put()
        if order_list:
            first_event = ConfigDB.gql("Where config_name =:1", order_list[0]['name']).get()
        else:
            first_event = ConfigDB.gql("Where config_name =:1", config_name).get()
        first_event.commence_test = True
        first_event.active_testplan_name = names[-1]
        first_event.put()
        start_time = datetime.datetime.now()
        key = db.Key.from_path('TestDB', names[-1], parent = company_key())
        testplan = db.get(key)
        testplan.start_time = start_time
        testplan.put()

        try:
            first_key = names[-1]+order_list[0]['type']+order_list[0]['name']
            key = db.Key.from_path('StateDB', first_key, parent = company_key())
            state_first_event = db.get(key)
            state_first_event.start_time = start_time
            state_first_event.put()
        except IndexError:
            logging.error("IndexError: State Event")

        self.redirect('/operator/{0}/{1}/{2}/{3}?testplan={4}'.format(
            company_nickname, hardware_name, config_name, start_tse, names[-1]))

class SaveResultsToTest():
    def post(self, results):
        pass

