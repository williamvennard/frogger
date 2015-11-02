from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import UserDB
from onedb import ProfileDB
import collections
import csv
import datetime
import hashlib
import itertools
import jinja2
import json
import logging
import os
import re
import time
import webapp2
import math
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
from collections import OrderedDict
import numpy as np
import appengine_config
import decimate
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from string import maketrans
from datetime import datetime

def getProfile():
	user = users.get_current_user()
	if user:
		q = ProfileDB.all().filter("userid =", user.user_id())
		profile = q.get()
		return profile
	else:
		return False	

class Handler(InstrumentDataHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			q = ProfileDB.all().filter("email =", user.email())
			profile = q.get()
			# complete the profile by syncing the userid
			if profile.userid != user.user_id():
				profile.userid = user.user_id()
				profile.put()
			self.set_groups_cookie()
			groups = self.request.cookies.get("groups")
			self.render('profile.html', profile=profile, groups=groups)
		else:
			self.redirect('/')