from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import TestDB
from onedb import TestDB_key
from onedb import DutDB
from onedb import DutDB_key
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
        dut_name = self.request.get('dut_name')
        dut_type = self.request.get('dut_type')
        settings = self.request.get('settings')
        testpost = (self.request.get('testpost'))
        instpost = (self.request.get('instpost'))
        dutpost = (self.request.get('dutpost'))

        if testpost == 'True': #this controls the POST functionality if someone is configuring test plan details.
            print 'hi'
            t = TestDB(parent = TestDB_key(testplan_name), 
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            test_plan = True,
            trace = False,
            )
            t.put() 
        if instpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            tests = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            inst = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            if inst == None:  #if there is not an instrument with the inputted name, then create it in the DB
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
            if inst == None:
                print 'no inst found the first time'
                inst = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            if tests.key() not in inst.tests:  #add the test plan to the list property of the instrument
                inst.tests.append(tests.key())
                inst.put()
            insts = ConfigDB.gql("Where instrument_name =:1", instrument_name).get()
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            if insts.key() not in test.instruments:  #add the instrument name to the list property ot the test plan
                test.instruments.append(insts.key())
                test.put()
        if dutpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            tests = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            dut = DutDB.gql("Where dut_name =:1", dut_name).get()
            if dut == None:  #if there is not an instrument with the inputted name, then create it in the DB
                d = DutDB(parent = DutDB_key(dut_name), 
                    company_nickname = company_nickname, author = author,
                    dut_type = dut_type,
                    dut_name = dut_name,             
                    settings = settings,
                    )
                d.put()
            dut = DutDB.gql("Where dut_name =:1", dut_name).get()
            if dut == None:
                print 'no dut found the first time'
                dut = DutDB.gql("Where dut_name =:1", dut_name).get()
            if tests.key() not in dut.tests:  #add the test plan to the list property of the dut
                dut.tests.append(tests.key())
                dut.put()
            duts = DutDB.gql("Where dut_name =:1", dut_name).get()
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            if duts.key() not in test.duts:  #add the  dut name to the list property ot the test plan
                test.duts.append(duts.key())
                test.put()    
        self.render('testconfig.html')
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)