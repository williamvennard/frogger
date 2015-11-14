from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import InstrumentsDB
from onedb import company_key
from onedb import CapabilitiesDB
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
        self.render('configlookup.html')
    def post(self):
        inst_info = self.request.body
        print inst_info
        new_inst_info = inst_info.split('&')
        new_inst_info = new_inst_info[0].split('=')
        print new_inst_info[1]
        if new_inst_info[1] == 'U2001A':
            model = self.request.get('model')
            company_nickname = self.request.get('company_nickname')
            hardware_name = self.request.get('hardware_name')
            instrument_type = self.request.get('instrument_type')
            serial_number = self.request.get('serial_number')
            channel_count = self.request.get('channel_count')
            frequency_low = self.request.get('frequency_low')
            frequency_high = self.request.get('frequency_high')
            power_low = self.request.get('power_low')
            power_high = self.request.get('power_high')
            instpost = self.request.get('instpost')
            cappost = self.request.get('cappost')
            instrument_type = self.request.get('instrument_type')
            bitscope = CapabilitiesDB(instrument_type = 'BitScope')
            print channel_count, frequency_high, frequency_high
            if instpost == 'True': #this controls the POST functionality if someone is configuring test plan details.
                instrument = InstrumentsDB(key_name = hardware_name, 
                             company_nickname = company_nickname, 
                             serial_number = serial_number, 
                             instrument_type = model,
                             hardware_name = hardware_name,
                             )
                capability = CapabilitiesDB.all().filter("instrument_type =", model).get()
                instrument.capabilities = capability
                instrument.put()
            if cappost == 'True': #this controls the POST functionality if someone is configuring test plan details.
                c = CapabilitiesDB(key_name = instrument_type, parent = company_key(),
                    instrument_type = instrument_type,
                    channel_count = int(channel_count), 
                    frequency_low = (frequency_low), 
                    frequency_high = frequency_high,
                    power_low = power_low,
                    power_high = power_high,
                    )
                c.put() 
        else:
            model = self.request.get('model')
            company_nickname = self.request.get('company_nickname')
            hardware_name = self.request.get('hardware_name')
            instrument_type = self.request.get('instrument_type')
            serial_number = self.request.get('serial_number')
            analog_bandwidth= self.request.get('analog_bandwidth')
            capture_channels = self.request.get('capture_channels')
            analog_sample_rate = self.request.get('analog_sample_rate')
            resolution = self.request.get('resolution')
            capture_buffer_size = self.request.get('capture_buffer_size')
            instpost = self.request.get('instpost')
            cappost = self.request.get('cappost')
            instrument_type = self.request.get('instrument_type')
            bitscope = CapabilitiesDB(instrument_type = 'BitScope')
            if instpost == 'True': #this controls the POST functionality if someone is configuring test plan details.
                instrument = InstrumentsDB(key_name = hardware_name, 
                             company_nickname = company_nickname, 
                             serial_number = serial_number, 
                             instrument_type = model,
                             hardware_name = hardware_name,
                             )
                capability = CapabilitiesDB.all().filter("instrument_type =", model).get()
                instrument.capabilities = capability
                instrument.put()
            if cappost == 'True': #this controls the POST functionality if someone is configuring test plan details.
                c = CapabilitiesDB(key_name = instrument_type, parent = company_key(),
                    instrument_type = instrument_type,
                    analog_bandwidth = int(analog_bandwidth), 
                    capture_channels = int(capture_channels), 
                    analog_sample_rate = int(analog_sample_rate),
                    resolution = int(resolution),
                    capture_buffer_size = int(capture_buffer_size),
                    )
                c.put() 
        self.render('configlookup.html')
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)