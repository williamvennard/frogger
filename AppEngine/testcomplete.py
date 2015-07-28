from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import render_json_cached
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import TestDB
from onedb import TestDB_key
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import company_key
from onedb import StateDB
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
import datetime
from string import maketrans

class Handler(InstrumentDataHandler):
    def post(self, company_nickname="", testplan_name="", config_name="", stop_tse=""):
        #key = 'testresults' + company_nickname + testplan_name + stop_tse
        test_complete_content = json.loads(self.request.body)
        print test_complete_content
        test_plan = test_complete_content['test_plan']
        if test_plan == 'True':   
            stop_time = datetime.datetime.now()
            key= testplan_name+'config'+config_name
            prior_key = db.Key.from_path('StateDB', key, parent = company_key())
            prior_event = db.get(prior_key)
            prior_event.stop_time = stop_time
            prior_event.put()     
            config_to_update = ConfigDB.gql("Where config_name =:1", config_name).get()
            config_to_update.commence_test = False
            config_to_update.active_testplan_name = None
            config_to_update.put()
            s = db.Query(StateDB)
            s.filter('company_nickname =', company_nickname).filter('testplan_name =', testplan_name).filter('start_time =', None).order('order')
            next_state = s.get()
            start_time = datetime.datetime.now()
            next_state.start_time = start_time
            next_config_name = next_state.name
            next_state.put()
            config_to_update = ConfigDB.gql("Where config_name =:1", next_config_name).get()
            config_to_update.commence_test = True
            config_to_update.active_testplan_name = testplan_name
            config_to_update.put()

            #state_table = StateDB.gql("Where company_nickname=:1 and testplan_name=:2 and start_time =:3", company_nickname, testplan_name, None).get()
            #ordered = state_table.order("order")
            
            #query and sort
           # set commence test to True
           # set start time
           # if none, 
           # test_plan = test_complete
            #to_save = []
            #r = TestResultsDB(parent = TestResultsDB_key(testplan_name), testplan_name=testplan_name,
            #        company_nickname = company_nickname, 
            #        Total_Slices=(test_complete_content['p_settings']['Total_Slices']),
            #        Dec_msec_btw_samples=(test_complete_content['p_settings']['Dec_msec_btw_samples']),
            ##        Raw_msec_btw_samples=(test_complete_content['p_settings']['Raw_msec_btw_samples']),
            #        Slice_Size_msec=(test_complete_content['p_settings']['Slice_Size_msec']),
            #        dec_data_url=str(test_complete_content['dec_data_url']),
            #        raw_data_url=str(test_complete_content['raw_data_url']),
            #        config_name=str(test_complete_content['config_name']),
            ##        hardware_name=str(test_complete_content['hardware_name']),
            #        test_plan = test_plan,
            #        test_complete_bool = True,
            #        test_complete = int(stop_tse),
            #        trace = trace, 
            ##        start_tse=(test_complete_content['start_tse'])
             #       )
            ##to_save.append(r) 
            #memcache.set(key, to_save)
            #db.put(to_save)
            #result = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", company_nickname, testplan_name)
            #for r in result:
            #    r.commence_test = False
            #    r.put()
           # update commence test to False, update stop time
           # db query for test , sort by start and stop = none, and order, flip bit to start_tse
           # result = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and testplan_name =:2", company_nickname, testplan_name)
           # for r in result:
           #     r.commence_test = False
           #     r.put()
        else:
            test_plan = False
            trace = True
            config_name = test_complete_content['config_name']
            hardware_name = test_complete_content['hardware_name']
            to_save = []
            r = TestResultsDB(parent = TestResultsDB_key(testplan_name), testplan_name=testplan_name,
                    company_nickname = company_nickname, 
                    Total_Slices=int(test_complete_content['p_settings']['Total_Slices']),
                    Dec_msec_btw_samples=(test_complete_content['p_settings']['Dec_msec_btw_samples']),
                    Raw_msec_btw_samples=(test_complete_content['p_settings']['Raw_msec_btw_samples']),
                    Slice_Size_msec=(test_complete_content['p_settings']['Slice_Size_msec']),
                    dec_data_url=str(test_complete_content['dec_data_url']),
                    raw_data_url=str(test_complete_content['raw_data_url']),
                    config_name=config_name,
                    hardware_name=hardware_name,
                    test_plan = test_plan,
                    test_complete_bool = True,
                    test_complete = int(stop_tse),
                    trace = trace, 
                    start_tse=(test_complete_content['start_tse']),
                    )
            to_save.append(r) 
            memcache.set(key, to_save)
            db.put(to_save)
            result = db.GqlQuery("SELECT * FROM ConfigDB WHERE config_name =:1 and hardware_name =:2 and company_nickname =:3 and testplan_name =:4", config_name, hardware_name, company_nickname, testplan_name)
            for r in result:
                r.commence_test = False
                r.put()