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
        hardware_name = config_data['hardware_name']
        instrument_type = config_data['inst_name']
        config_name = config_data['config_name']
        analog_sample_rate = int(config_data['analog_sample_rate'])
        testplan_name = config_data['trace_name']
        key_name = config_name + testplan_name
        capture_buffer_size = int(config_data['capture_buffer_size'])
        if instrument_type == 'BitScope':
            analog_bandwidth == 20000000
        c = ConfigDB(key_name = (config_name+testplan_name), parent = company_key(),
                company_nickname = company_nickname, author = author,
                capture_channels = capture_channels,
                analog_sample_rate = analog_sample_rate,
                analog_bandwidth = analog_bandwidth,
                resolution = resolution,
                capture_buffer_size = capture_buffer_size,
                instrument_type = instrument_type,
                hardware_name = hardware_name,
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

