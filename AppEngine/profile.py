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

	def set_groups_cookie(self):
		profile = getProfile()
		if hasattr(profile, 'groups'):         
			groups_string = "|".join(profile.groups)            
			self.response.set_cookie('groups', groups_string)
			return True
		else:
			return False


class AdduserPage(InstrumentDataHandler):
    def get(self):
        profile = getProfile()
        if profile.admin:
            admin_email = profile.email
            self.render('adduser.html')            
        else:
            self.redirect('/')

    def post(self):
        email = self.request.get('email')
        companyname = self.request.get('companyname')
        name = self.request.get('name')
        # TODO - handle spaces in companyname
        profile = ProfileDB(email = email, 
                      company_nickname = companyname, 
                      name = name)
        profile.put()
        checked_box = self.request.get("admin")
        if checked_box:
            profile.admin = True
        else:
            profile.admin = False
        if not profile.bio:
            profile.bio = "No bio entered yet."
        profile.put()
        self.redirect('/profile')


class ListUsersPage(InstrumentDataHandler):
    def get(self):
        profile = getProfile()
        if not profile.admin:
            redirect('/')
        users = db.GqlQuery("SELECT * FROM ProfileDB WHERE company_nickname = 'GradientOne'").fetch(None)
        print "ListUsersPage:get: users =",users
        if len(users) > 0:
            self.render('listusers.html',company=users[0].company_nickname,
                        users=users)
        else:
            self.render('listusers.html',company="new company?",
                        users=users)
    def post(self):
        email = self.request.get('user_email')
        q = ProfileDB.all().filter("email =", email)
        profile = q.get()

        group = self.request.get('group')
        profile.groups.append(group)
        profile.put()

        group_to_delete = self.request.get('group_to_delete')
        profile.groups.remove(group_to_delete)
        profile.put()
        profile.groups = filter(None, profile.groups)
        profile.put()

        self.redirect('/listusers')