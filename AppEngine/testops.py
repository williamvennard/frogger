from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
from onedb import TestInterface
from onedb import TestDB
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
from profile import getProfile
import appengine_config
import json


class Handler(InstrumentDataHandler):
	def get(self):
		profile = getProfile()
		query = TestDB.all().filter("company_nickname =", profile.company_nickname)
		tests = query.run()
		query = ConfigDB.all().filter("company_nickname =", profile.company_nickname)
		configs = query.run()
		self.render('ops.html', tests=tests, configs=configs)
	def post(self):
		configKey = self.request.get('configKey')
		config = db.get(configKey)
		testplan = self.request.get('test')
		test = TestDB.all().filter("testplan_name =", testplan).get()
		data = {
			'config': "default",
			'company_nickname' : test.company_nickname,
			'hardware_name' : test.hardware_name,
			'config_name' : config.config_name,
			'start_tse' : "0",
			'instrument' : "default",
		}
		self.redirect('/operator/{0}/{1}/{2}/{3}/{4}?testplan={5}'.format(
            test.company_nickname, test.hardware_name, config.config_name, 
            '0', 'bscope',test.testplan_name))