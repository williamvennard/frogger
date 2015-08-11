from gradientone import InstrumentDataHandler
from gradientone import author_creation
from onedb import ConfigDB
from onedb import company_key
import json
import itertools
import jinja2
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self):
        self.render('bscopeconfiginput.html')
    def is_checked(self,c,param):
        "Mesurement checked and up date test object 'c'."
        checked = self.request.get(param)
        if checked:
            setattr(c,param,True)
        else:
            setattr(c,param,False)
    def post(self):
        author = author_creation()
        config_data = json.loads(self.request.body)
        print config_data
        company_nickname = config_data['company_nickname']
        hardware = config_data['hardware_name']
        instrument_type = config_data['inst_type']
        config_name = config_data['config_name']
        sample_rate = int(config_data['sample_rate'])
        testplan_name = config_data['trace_name']
        key_name = config_name + testplan_name
        number_of_samples = int(config_data['number_of_samples'])
        print config_name, company_nickname, author, hardware_name, instrument_type, number_of_samples, sample_rate, testplan_name
        c = ConfigDB(key_name = (config_name+testplan_name), parent = company_key(),
                company_nickname = company_nickname, author = author,
                analog_bandwidth = analog_bandwidth,
                capture_channels = capture_channels,
                analog_sample_rate = analog_sample_rate,
                resolution = resolution,
                capture_buffer_size = capture_buffer_size,
                instrument_type = instrument_type,
                hardware_name = hardware,
                test_plan = True,
                active_testplan_name = testplan_name,
                trace = False,
                )
        c.put() 
        checkbox_names = ["commence_test", "commence_explore"]
        for name in checkbox_names:
            self.is_checked(c,name)
            print c
        c.put()
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + config_name
        memcache.delete(key)
        self.redirect('/configoutput/' + (author + '/' + instrument_type + '/' + config_name))



