from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from gradientone import query_to_dict
from gradientone import convert_str_to_cha_list
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
import itertools
import jinja2
import webapp2
import logging
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
import json

result_types = {
    'bscope' : BscopeDB,
    'aU2000' : agilentU2000data
}

class Handler(InstrumentDataHandler):

    def get(self,company_nickname="", hardware_name="",config_name="",
        start_tse="",instrument=""):
        "retrieve instrument data by instrument name and time slice name"
        # if not self.authcheck():
        #     return
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
                'instrument' : instrument,
                }

        # resultKey = BscopeDB_key(company_nickname, config_name)
        # result = BscopeDB.get(resultKey)

        query = result_types[instrument].all().filter("company_nickname =", company_nickname)
        query = query.filter("config_name =", config_name)
        result = query.get()
        comment_thread = []
        if hasattr(result, 'comments'):
            for comment in result.comments:
                comment_thread.append(comment)

        templatedata['comment_thread'] = comment_thread
    
        key = instrument + company_nickname + hardware_name + config_name + start_tse
        cached_copy = memcache.get(key)
        if cached_copy is None:

            result_data = result_types[instrument].all().get()
            data = result_data.to_dict()
            if not data:
                logging.error("ResultData:get: query")
                templatedata['results'] = "Error: No result data"
                self.render('operator.html', data=templatedata)
            if instrument == 'bscope':
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

    def post(self, company_nickname="", hardware_name="",config_name="",
        start_tse="",instrument=""):
        user = users.get_current_user()
        if not user.nickname():
            author = "anonymous"
        else:
            author = user.nickname()
        content = self.request.get('content')
        query = result_types[instrument].all().filter("company_nickname =", company_nickname)
        query = query.filter("config_name =", config_name)
        result_data = query.get()
        comment = CommentsDB(author=author, content=content, results=result_data)
        comment.put()
        self.redirect('/operator/{0}/{1}/{2}/{3}/{4}'.format(
            company_nickname, hardware_name, config_name, start_tse, instrument))

class Special(InstrumentDataHandler):
    def post(self,company_nickname="", hardware_name="", config_name="",
    		 start_tse="", instrument=""):
        "store data by instrument name and time slice name"
        #key = instrument + company_nickname + hardware_name + config_name + start_tse
        #memcache.set(key, self.request.body)
        test_results = json.loads(self.request.body)
        test_results_data = test_results['cha']
        data_length = len(test_results_data)
        slice_size = int(test_results['p_settings']['Slice_Size_msec'])
        sample_rate = int(test_results['i_settings']['Sample_Rate_Hz'])
        test_plan = test_results['test_plan']
        testplan_name = test_results['testplan_name']
        print testplan_name
        sample_per_slice = int((float(sample_rate)/1000)*float(slice_size))
        print slice_size, sample_rate, sample_per_slice
        print data_length
        start_tse = int(start_tse)
        stuffing = []
        for i in range(0, data_length, sample_per_slice):
            chunk = str(test_results_data[i:i + sample_per_slice])
            stuffing = chunk
            key = instrument + company_nickname + hardware_name + config_name + str(start_tse)
            print key
            stuffing = convert_str_to_cha_list(stuffing)
            window_instrument = {'i_settings':test_results['i_settings'], 'p_settings':test_results['p_settings'], 'cha':stuffing, 'testplan_name':testplan_name,
            'start_tse':start_tse, 'company_nickname':company_nickname, 'start_tse':start_tse, 'hardware_name':hardware_name, 'config_name':config_name, 'test_plan':test_plan}
            out_instrument = json.dumps(window_instrument, ensure_ascii=True)
            memcache.set(key, out_instrument)
            start_tse += slice_size
