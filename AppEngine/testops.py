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
from profile import get_profile_cookie
import appengine_config
import json


class Handler(InstrumentDataHandler):
	def get(self):
		profile = get_profile_cookie(self)
		print "PROFILE: ", profile
		if (not profile) or (profile['permissions'] == "viewer"):
			print "Invalid Permissions"
			self.redirect('/profile')
		else:
			configs = []
			if profile.has_key('company_nickname'):
				query = TestDB.all().filter("company_nickname =", profile['company_nickname'])
				query = query.filter("ops_start =", True)
				tests = query.run()
				for test in tests:
					for config_key in test.configs:
						config = db.get(config_key)
						config.active_testplan_name = test.testplan_name #temp fix to correct displayname TODO- align tests and configs names
						configs.append(config)
				self.render('ops.html', configs=configs, profile=profile)
			else:
				self.render('ops.html', configs=configs, profile=profile)
	def post(self):
		configKey = self.request.get('configKey')
		config = db.get(configKey)
		testplan = self.request.get('test')
		test = TestDB.all().filter("testplan_name =", testplan).get()
		self.redirect('/operator/{0}/{1}/{2}'.format(
            test.company_nickname, config.config_name, test.testplan_name))