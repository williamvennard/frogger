from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
from onedb import TestInterface
import itertools
import jinja2
import webapp2
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
import json

class Handler(InstrumentDataHandler):
    def get(self):
        self.render('test_make_interface.html')

    def post(self):
      # get data from form and create object
      data = {}
      attributes = ['title', 
                    'company_nickname', 
                    'instrument_type', 
                    'config_name',
                    'trace_name',
                    ]
      for attribute in attributes:
          data[attribute] = self.request.get(attribute)
      test_interface = TestInterface(**data)
      # test_interface.put()
      key = data['title']+data['company_nickname']
      memcache.set(key, json.dumps(data))

      # for debugging
      render_json_cached(self, json.dumps(data))

      # ToDo - when operator is complete, page should redirect there
      # self.redirect('/operator')