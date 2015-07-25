from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import TestDB
from onedb import TestDB_key
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self):
        #if not self.authcheck():
        #    return
        self.render('testconfig.html')
    def is_checked(self,t,param):
        "Test checked and up date test object 't'."
        checked = self.request.get(param)
        if checked:
            setattr(t,param,True)
        else:
            setattr(t,param,False)
    def post(self):
        configs = []
        testplan_name = self.request.get('testplan_name')
        company_nickname = self.request.get('company_nickname')
        author = self.request.get('author')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        hardware_name = self.request.get('hardware_name')
        RMS_time_start = (self.request.get('RMS_time_start'))
        RMS_time_stop = (self.request.get('RMS_time_stop'))
        sample_rate = (self.request.get('sample_rate'))
        number_of_samples = (self.request.get('number_of_samples'))
        testpost = (self.request.get('testpost'))
        instpost = (self.request.get('instpost'))
        if testpost == 'True':
            print 'hi'
            t = TestDB(parent = TestDB_key(testplan_name), 
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            test_plan = True,
            trace = False,
            )
            t.put()  # might help with making plan show up on list?
        if instpost == 'True':
            tests = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            inst = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            print inst
            if inst == None:
                c = ConfigDB(parent = ConfigDB_key(instrument_name), 
                    company_nickname = company_nickname, author = author,
                    hardware_name = hardware_name, instrument_type = instrument_type,
                    instrument_name = instrument_name,             
                    sample_rate = int(sample_rate), number_of_samples = int(number_of_samples),
                    test_plan = True,
                    trace = False,
                    )
                c.put()
            inst = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            print inst
            if tests.key() not in inst.tests:
                inst.tests.append(tests.key())
                inst.put()
            insts = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            if insts.key() not in test.instruments:
                test.instruments.append(insts.key())
                test.put()


            #c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            #company_nickname = company_nickname, author = author,
            #hardware_name = hardware_name, instrument_type = instrument_type,
            #instrument_name = instrument_name,             
            #sample_rate = int(sample_rate), number_of_samples = int(number_of_samples),
            #test_plan = True,
            #testplan_name = testplan_name,
            ##trace = False,
            #)
            #c.put()


        
        self.render('testconfig.html')
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)