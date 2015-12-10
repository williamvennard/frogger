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
from onedb import BlobberDB
import itertools
import jinja2
import json
import logging
import os
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.api import search
from google.appengine.ext import db
import appengine_config
import datetime
from string import maketrans
import docs
import searchconfig

class Handler(InstrumentDataHandler):
    def post(self, company_nickname="", testplan_name="", config_name="", stop_tse=""):
        test_complete_content = json.loads(self.request.body)
        test_plan = test_complete_content['test_plan']
        i_settings = test_complete_content['i_settings']
        logging.debug("TEST_CONTENT: %s" % test_complete_content)
        if test_plan == 'True':   
            stop_time = datetime.datetime.now()
            key = testplan_name+'U2001A'+config_name
            prior_key = db.Key.from_path('StateDB', key, parent = company_key())
            prior_event = db.get(prior_key)
            prior_event.stop_time = stop_time
            prior_event.put()     
            config_to_update = ConfigDB.get(ConfigDB_key(config_name))
            config_to_update.commence_test = False
            config_to_update.active_testplan_name = None
            config_to_update.put()
            s = db.Query(StateDB)
            s.filter('company_nickname =', company_nickname).filter('testplan_name =', testplan_name).filter('start_time =', None).order('order')
            next_state = s.get()
            to_save = []
            key = 'TestResultsDB'+testplan_name+config_name
            test_plan = True
            trace = False
            hardware_name = test_complete_content['hardware_name']
            r = TestResultsDB(parent = company_key(), testplan_name=testplan_name, key_name = key,
                    company_nickname = company_nickname, 
                    config_name=config_name,
                    hardware_name=hardware_name,
                    test_plan = test_plan,
                    test_complete_bool = True,
                    test_complete = int(stop_tse),
                    trace = trace, 
                    start_tse=(test_complete_content['start_tse']),
                    u2000_result = str(test_complete_content['cha']),
                    )
            to_save.append(r) 
            db.put(to_save)
            if next_state == None:
                key = db.Key.from_path('TestDB', testplan_name, parent = company_key())
                testplan = db.get(key)
                testplan.stop_time = stop_time
                testplan.put()
            else:
                start_time = datetime.datetime.now()
                next_state.start_time = start_time
                next_config_name = next_state.name
                next_state.put()
                config_to_update = ConfigDB.get(ConfigDB_key(next_config_name))
                config_to_update.commence_test = True
                config_to_update.active_testplan_name = testplan_name
                config_to_update.put()

        else:
            test_plan = False
            trace = True
            config_name = test_complete_content['config_name']
            hardware_name = test_complete_content['hardware_name']
            to_save = []
            key = testplan_name + str(test_complete_content['start_tse'])
            logging.debug("TRACE COMPLETE - KEY: %s" % key)
            logging.debug("TRACE COMPLETE - CONTENT: %s" % test_complete_content)
            r = TestResultsDB(parent = company_key(), testplan_name=testplan_name, key_name = key,
                    company_nickname = company_nickname, 
                    config_name=config_name,
                    hardware_name=hardware_name,
                    test_plan = test_plan,
                    test_complete_bool = True,
                    test_complete = int(stop_tse),
                    trace = trace, 
                    start_tse=(test_complete_content['start_tse']),
                    u2000_result = str(test_complete_content['cha']),
                    )
            to_save.append(r) 
            db.put(to_save)
        # Testplan or not, index the results    
        blobber_key = db.Key.from_path('BlobberDB', testplan_name, parent = company_key())
        the_blob = BlobberDB.get(blobber_key)
        logging.debug("THE BLOB!!! %s" % the_blob)
        blob_key = the_blob.b_key
        fields = [ 
            search.DateField(name=docs.U2000.START_TSE, 
                value=datetime.datetime.fromtimestamp(
                    int(test_complete_content['start_tse'])/1000
                    )),
            search.NumberField(name=docs.U2000.CORRECTION_FREQ, value=float(i_settings['correction_frequency'])), 
            search.NumberField(name=docs.U2000.MAX_VALUE, value=float(i_settings['max_value'])), 
            search.NumberField(name=docs.U2000.MIN_VALUE, value=float(i_settings['min_value'])), 
            search.NumberField(name=docs.U2000.OFFSET, value=float(i_settings['offset'])), 
            search.TextField(name=docs.U2000.PASS_FAIL_TYPE, value=i_settings['pass_fail_type']),
            search.TextField(name=docs.U2000.TEST_PLAN, value=test_complete_content['test_plan']),
            search.TextField(name=docs.U2000.PASS_FAIL, value=i_settings['pass_fail']),
            search.TextField(name=docs.U2000.HARDWARE_NAME, value=hardware_name),
            search.TextField(name=docs.U2000.DATA, value=str(test_complete_content['cha'])),
            search.TextField(name=docs.U2000.INSTRUMENT_TYPE, value='U2000'),
            search.TextField(name=docs.U2000.CONFIG_NAME, value=config_name),
            search.TextField(name=docs.U2000.TESTPLAN_NAME, value=test_complete_content['active_testplan_name']),
        ]        
        d = search.Document(doc_id=blob_key, fields=fields)
        try:
            add_result = search.Index(name=searchconfig.U2000_INDEX_NAME).put(d)
            logging.debug("INDEXED IN %s" % searchconfig.U2000_INDEX_NAME)
        except search.Error:
            logging.exception("Search error adding document")
            #memcache.set(key, to_save)


            #Done - refactored docs.py to work with U2000 code
            #Done - added a searchconfig.py file for search configurations
            #Done - identified location for and placed Index creation code
            #Done - enter in extra fields for U2000
            #TODO - update U2000_client and U2000_post to post config data along with results to server
            #TODO - write queryhandlers or refactor google example code to work with gradientone code


class UpdateResults(InstrumentDataHandler):
    """Called from testops.js to update results with pass_fail data"""
    def post(self):
        results_data = json.loads(self.request.body)
        config_name = results_data['config_name']
        trace_name = results_data['trace_name']
        start_tse = results_data['start_tse']
        pass_fail = results_data['pass_fail']
        min_pass = results_data['min_pass_value']
        max_pass = results_data['max_pass_value']
        key = trace_name + str(start_tse) + pass_fail
        cached_result = memcache.get(key)
        key_name = trace_name + str(start_tse)
        test_key = db.Key.from_path('TestResultsDB', key_name, parent=company_key())
        if not cached_result:
            test_results = TestResultsDB.get(test_key)
            test_results.pass_fail = pass_fail
            test_results.min_pass = float(min_pass)
            test_results.max_pass = float(max_pass)
            test_results.put()
            memcache.set(key, test_results)



