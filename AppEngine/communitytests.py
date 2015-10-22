from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import TestDB
from onedb import TestResultsDB
from onedb import CommunityPostDB
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

class Handler(InstrumentDataHandler):
	def get(self):
		user = users.get_current_user()
		q = ProfileDB.all().filter("email =", user.email())
		profile = q.get()
		tests = TestDB.all()

		if not profile.company_nickname:
			company_nickname = "No_Company"
		else:
			company_nickname = profile.company_nickname
		tests.filter("company_nickname =", company_nickname)
		
        # Get all posts
		public_posts = CommunityPostDB.all().order('-date_created')

	   	if profile:
			# Limit to posts of user's company and group posts
			filterlist = []
			filterlist.append("company")
			filterlist.extend(profile.groups)
			group_posts = CommunityPostDB.all().order('-date_created')
			group_posts.filter("privacy IN", filterlist)
			group_posts.filter("company_nickname =", profile.company_nickname)

			# Limit to public posts
			public_posts.filter("privacy =", "public")
			self.render('communitytests.html', group_posts=group_posts, 
						public_posts=public_posts, tests=tests, p_count=0, 
						g_count=0, groups=profile.groups)
		else:
			# Limit to just public posts
			public_posts = public_posts.filter("privacy =", "public")
			public_posts.filter("privacy =", "public")
			self.render('communitytests.html', public_posts=public_posts, 
						tests=tests, p_count=0, groups=profile.groups)

	def post(self):
		user = users.get_current_user()
		q = ProfileDB.all().filter("email =", user.email())
		profile = q.get()

		# get user requested test to post 
		testkey = self.request.get("testkey")
		test = db.get(testkey)

		title = self.request.get("title")
		privacy = self.request.get("privacy")
		
		if not profile:
			company_nickname = "No_Company"
		else:
			company_nickname = profile.company_nickname
		# Create CommunityPostDB object from test
		newpost = CommunityPostDB(title=title,
								  author=user.nickname(),
								  test_ref=test,
								  privacy=privacy,
								  company_nickname=company_nickname,
								  )
		newpost.put()

		self.redirect("/community")

class SavePostToTest(InstrumentDataHandler):

	def clone_entity(self, e, **extra_args):
		"""Clones an entity, adding or overriding constructor attributes.

		The cloned entity will have exactly the same property values as the original
		entity, except where overridden. By default it will have no parent entity or
		key name, unless supplied.

		Args:
		e: The entity to clone
		extra_args: Keyword arguments to override from the cloned entity and pass
		  to the constructor.
		Returns:
		A cloned, possibly modified, copy of entity e.
		"""
		klass = e.__class__
		props = dict((k, v.__get__(e, klass)) for k, v in klass.properties().iteritems())
		props.update(extra_args)
		return klass(**props)


	def post(self):
		"""Clones the selected testpost and saves the test to the library with
		a new company_nickname for the user to view later"""

		session_user = users.get_current_user()
		q = ProfileDB.all().filter("email =", session_user.email())
		profile = q.get()

		postkey = self.request.get("postkey")
		testpost = db.get(postkey)

		if not profile:
			company_nickname = "No_Company"
		else:
			company_nickname = profile.company_nickname

		# Check if test company is same as users. If so skip saving as it is already in library
		if testpost.test_ref.company_nickname == company_nickname:
			self.redirect("/community")
		else:
			saved_test = self.clone_entity(testpost.test_ref, company_nickname=company_nickname)
			saved_test.put()
			self.redirect("/community")		


class PrivateHandler(InstrumentDataHandler):
	def get (self):
		user = users.get_current_user()

        # Get all posts 
		posts = CommunityPostDB.all().order('-date_created')
		# Limit to just public posts
		posts.filter("privacy =", "private")
		posts.filter("author =", user.nickname())

		tests = TestDB.all()

		self.render('communitytests.html', posts=posts, tests=tests, counter=6)
