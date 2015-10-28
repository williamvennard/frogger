from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from gradientone import query_to_dict
from gradientone import convert_str_to_cha_list
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
from onedb import TestInterface
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


class Handler(InstrumentDataHandler):
    def get(self,company_nickname="", hardware_name="",config_name="",
        slicename="",instrument=""):
        "retrieve instrument data by instrument name and time slice name"
        #if not self.authcheck():
        #    return
        testkey = 'T1'+'GradientOne'
        test = memcache.get(testkey)
        if test is None:
            logging.error("TestData:get: query")
            test = '{"instrument_type": "sample inputs", "config_name": "config1", "company_nickname": "GradientOne", "trace_name": "trace1", "title": "T1"}'
        key = instrument + company_nickname + hardware_name + config_name + slicename
        cached_copy = memcache.get(key)
        # if cached_copy is None:
        templatedata = {
                'test': test,
                'company_nickname' : company_nickname,
                'hardware_name' : hardware_name,
                'config_name' : config_name,
                }  
        if True:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB""")
            # rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE config_name =:1
                                # AND slicename = :2""", config_name, slicename)  
            rows = list(rows)
            data = query_to_dict(rows)
            print data[0]
            cha_list = convert_str_to_cha_list(data[0]['cha'])
            data[0]['cha'] = cha_list
            e = data[0]
            print e
            print type(e)
            output = {"data":data[0]}
            output = json.dumps(e)
            memcache.set(key, output)
            templatedata['results'] = output
            self.render('operator.html', data=templatedata)
            #render_json_cached(self, output)
        else:
            templatedata['results'] = cached_copy
            self.render('operator.html', data=templatedata)
            #render_json_cached(self, cached_copy)

    def post(self, company_nickname="", hardware_name="",config_name=""):
        user = users.get_current_user()
        if not user.nickname():
            author = "anonymous"
        else:
            author = user.nickname()
        content = self.request.get('content')
        resultKey = BscopeDB_key(company_nickname, config_name)
        Bscope = db.get(resultKey)
        comment = CommentsDB(author=author, content=content, results=Bscope)
        comment.put()
        self.redirect('/operator/%s/%s/%s' % (company_nickname, hardware_name, config_name))

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
        slicename = int(start_tse)
        stuffing = []
        for i in range(0, data_length, sample_per_slice):
            chunk = str(test_results_data[i:i + sample_per_slice])
            stuffing = chunk
            key = instrument + company_nickname + hardware_name + config_name + str(slicename)
            print key
            stuffing = convert_str_to_cha_list(stuffing)
            window_instrument = {'i_settings':test_results['i_settings'], 'p_settings':test_results['p_settings'], 'cha':stuffing, 'testplan_name':testplan_name,
            'start_tse':start_tse, 'company_nickname':company_nickname, 'slicename':slicename, 'hardware_name':hardware_name, 'config_name':config_name, 'test_plan':test_plan}
            out_instrument = json.dumps(window_instrument, ensure_ascii=True)
            memcache.set(key, out_instrument)
            slicename += slice_size
