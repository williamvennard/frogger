from gradientone import InstrumentDataHandler
from gradientone import author_creation
from onedb import ConfigDB
from onedb import ConfigDB_key
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
        #if not self.authcheck():
         #   return
        self.render('configinput.html')
    def post(self):
        author = author_creation()
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        source = self.request.get('source')
        horizontal_position = float(self.request.get('horizontal_position'))
        horizontal_seconds_per_div = float(self.request.get('horizontal_seconds_per_div'))
        vertical_position = float(self.request.get('vertical_position'))
        vertical_volts_per_divsision = float(self.request.get('vertical_volts_per_divsision'))
        trigger_type = self.request.get('trigger_type')
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, 
            hardware_name = hardware_name, instrument_type = instrument_type, 
            instrument_name = instrument_name, source = source, 
            horizontal_position = horizontal_position, author = author,
            horizontal_seconds_per_div = horizontal_seconds_per_div, 
            vertical_position = vertical_position, 
            vertical_volts_per_division = vertical_volts_per_divsision, 
            trigger_type= trigger_type)
        c.put() 
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        memcache.delete(key)
        self.redirect('/configoutput/' + (author + '/' + instrument_type + '/' + instrument_name))