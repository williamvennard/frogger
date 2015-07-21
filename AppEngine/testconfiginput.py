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
        testplan_name = self.request.get('testplan_name')
        company_nickname = self.request.get('company_nickname')
        author = self.request.get('author')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        hardware_name = self.request.get('hardware_name')
        RMS_time_start = float(self.request.get('RMS_time_start'))
        RMS_time_stop = float(self.request.get('RMS_time_stop'))
        sample_rate = int(self.request.get('sample_rate'))
        number_of_samples = int(self.request.get('number_of_samples'))
        t = TestDB(parent = TestDB_key(testplan_name), 
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            instrument_type = instrument_type,
            RMS_time_start = RMS_time_start,
            test_plan = True,
            trace = False,
            RMS_time_stop = RMS_time_stop,)
        t.put()  # might help with making plan show up on list?
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name,             
            sample_rate = sample_rate, number_of_samples = number_of_samples,
            test_plan = True,
            testplan_name = testplan_name,
            trace = False,
            )
        c.put() 
        key = testplan_name
        memcache.delete(key)
        checkbox_names_test = ["measurement_P2P", "measurement_Peak",
                          "measurement_RMS", "measurement_RiseT",
                           "public", "commence_test"]
        for name in checkbox_names_test:
            self.is_checked(t,name)
        t.put()
        checkbox_names_config = ["commence_test"]
        for name in checkbox_names_config:
            self.is_checked(c,name)
        c.put()
        self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)