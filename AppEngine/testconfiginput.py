from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import ConfigDB
from onedb import company_key
from onedb import TestDB
from onedb import DutDB
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
        config_name = self.request.get('config_name')
        hardware_name = self.request.get('hardware_name')
        RMS_time_start = (self.request.get('RMS_time_start'))
        RMS_time_stop = (self.request.get('RMS_time_stop'))
        sample_rate = (self.request.get('sample_rate'))
        number_of_samples = (self.request.get('number_of_samples'))
        dut_name = self.request.get('dut_name')
        dut_type = self.request.get('dut_type')
        settings = self.request.get('settings')
        testpost = (self.request.get('testpost'))
        confpost = (self.request.get('confpost'))
        dutpost = (self.request.get('dutpost'))
        if testpost == 'True': #this controls the POST functionality if someone is configuring test plan details.
            t = TestDB(key_name = testplan_name, parent = company_key(),
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            test_plan = True,
            trace = False,
            )
            t.put() 
        if confpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            conf = ConfigDB.gql("Where config_name =:1", config_name).get() #add company name key
            if conf == None:  #if there is not an instrument with the inputted name, then create it in the DB
                c = ConfigDB(key_name = config_name, parent = company_key(), company_nickname = company_nickname, author = author,
                    hardware_name = hardware_name, instrument_type = instrument_type,
                    config_name = config_name,             
                    sample_rate = int(sample_rate), number_of_samples = int(number_of_samples),
                    test_plan = True,
                    trace = False,
                    )
                c.put()
            key = db.Key.from_path('ConfigDB', config_name, parent = company_key())
            conf = db.get(key)
            if test.key() not in conf.tests:  #add the test plan to the list property of the instrument
                conf.tests.append(test.key())
                conf.put()
            if conf.key() not in test.configs:  #add the instrument name to the list property ot the test plan
                test.configs.append(conf.key())
                test.put()
        if dutpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            dut = DutDB.gql("Where dut_name =:1", dut_name).get()
            if dut == None:  #if there is not an instrument with the inputted name, then create it in the DB
                d = DutDB(key_name = dut_name, parent = company_key(),
                    company_nickname = company_nickname, author = author,
                    dut_type = dut_type,
                    dut_name = dut_name,             
                    settings = settings,
                    )
                d.put()
            key = db.Key.from_path('DutDB', dut_name, parent = company_key())
            dut = db.get(key)
            if test.key() not in dut.tests:  #add the test plan to the list property of the dut
                dut.tests.append(test.key())
                dut.put()
            if dut.key() not in test.duts:  #add the  dut name to the list property ot the test plan
                test.duts.append(dut.key())
                test.put()    
        self.render('testconfig.html')
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)