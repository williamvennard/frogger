from gradientone import InstrumentDataHandler
from gradientone import author_creation
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
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

class Handler(InstrumentDataHandler):
    def get(self):
        self.render('test_make_interface.html')

    def post():
    	# get data from form
    	company_nickname = self.request.get('company_nickname')
    	....

    	# create model
    	config = ConfigDB(company_nickname,...)
    	config.put()


