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
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        sample_rate = int(self.request.get('sample_rate'))
        testplan_name = self.request.get('testplan_name')
        number_of_samples = int(self.request.get('number_of_samples'))
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name,             
            sample_rate = sample_rate, number_of_samples = number_of_samples,
            test_plan = False,
            testplan_name = testplan_name,
            trace = True,
            )
        c.put() 
        checkbox_names = ["commence_test"]
        for name in checkbox_names:
            self.is_checked(c,name)
        c.put()
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        memcache.delete(key)
        self.redirect('/configoutput/' + (author + '/' + instrument_type + '/' + instrument_name))


