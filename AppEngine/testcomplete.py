from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import render_json_cached
from gradientone import author_creation
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import TestDB
from onedb import TestDB_key
from onedb import ConfigDB
from onedb import ConfigDB_key
import itertools
import jinja2
import json
import logging
import os
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
from string import maketrans

class Handler(InstrumentDataHandler):
    def post(self, company_nickname="", testplan_name="", stop_tse=""):
        key = 'testresults' + company_nickname + testplan_name + stop_tse
        test_complete_content = json.loads(self.request.body)
        test_plan = test_complete_content['test_plan']
        if test_plan == 'True':        
            test_plan = True
            trace = False
            to_save = []
            r = TestResultsDB(parent = TestResultsDB_key(testplan_name), testplan_name=testplan_name,
                    company_nickname = company_nickname, 
                    Total_Slices=(test_complete_content['p_settings']['Total_Slices']),
                    Dec_msec_btw_samples=(test_complete_content['p_settings']['Dec_msec_btw_samples']),
                    Raw_msec_btw_samples=(test_complete_content['p_settings']['Raw_msec_btw_samples']),
                    Slice_Size_msec=(test_complete_content['p_settings']['Slice_Size_msec']),
                    dec_data_url=str(test_complete_content['dec_data_url']),
                    raw_data_url=str(test_complete_content['raw_data_url']),
                    instrument_name=str(test_complete_content['instrument_name']),
                    hardware_name=str(test_complete_content['hardware_name']),
                    test_plan = test_plan,
                    test_complete_bool = True,
                    test_complete = int(stop_tse),
                    trace = trace, 
                    start_tse=(test_complete_content['start_tse'])
                    )
            to_save.append(r) 
            memcache.set(key, to_save)
            db.put(to_save)
            result = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", company_nickname, testplan_name)
            for r in result:
                r.commence_test = False
                r.put()
            result = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and testplan_name =:2", company_nickname, testplan_name)
            for r in result:
                r.commence_test = False
                r.put()
        else:
            test_plan = False
            trace = True
            instrument_name = test_complete_content['instrument_name']
            hardware_name = test_complete_content['hardware_name']
            to_save = []
            r = TestResultsDB(parent = TestResultsDB_key(testplan_name), testplan_name=testplan_name,
                    company_nickname = company_nickname, 
                    Total_Slices=(test_complete_content['p_settings']['Total_Slices']),
                    Dec_msec_btw_samples=(test_complete_content['p_settings']['Dec_msec_btw_samples']),
                    Raw_msec_btw_samples=(test_complete_content['p_settings']['Raw_msec_btw_samples']),
                    Slice_Size_msec=(test_complete_content['p_settings']['Slice_Size_msec']),
                    dec_data_url=str(test_complete_content['dec_data_url']),
                    raw_data_url=str(test_complete_content['raw_data_url']),
                    instrument_name=instrument_name,
                    hardware_name=hardware_name,
                    test_plan = test_plan,
                    test_complete_bool = True,
                    test_complete = int(stop_tse),
                    trace = trace, 
                    start_tse=(test_complete_content['start_tse'])
                    )
            to_save.append(r) 
            memcache.set(key, to_save)
            db.put(to_save)
            result = db.GqlQuery("SELECT * FROM ConfigDB WHERE instrument_name =:1 and hardware_name =:2 and company_nickname =:3 and testplan_name =:4", instrument_name, hardware_name, company_nickname, testplan_name)
            for r in result:
                r.commence_test = False
                r.put()