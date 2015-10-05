from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import TestDB
from onedb import TestDB_key
from onedb import UserDB
from onedb import CommunityPostDB
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

class Handler(InstrumentDataHandler):
	def get(self):
		session_user = users.get_current_user()
		q = UserDB.all().filter("email =", session_user.email())
		user = q.get()
		tests = TestDB.all()
        # Get all posts
		posts = CommunityPostDB.all().order('-date_created')
	   	if user:
			# Limit to posts of user's company and public posts
			p1 = posts.filter("privacy IN", (user.company_nickname, "public"))
			self.render('communitytests.html', posts=posts, tests=tests, counter=6)
		else:
			# Limit to just public posts
			posts.filter("privacy =", "public")
			self.render('communitytests.html', posts=posts, tests=tests, counter=6)

	def post(self):
		user = users.get_current_user()

		# get user requested test to post 
		testkey = self.request.get("test")
		q = TestDB.all().filter('__key__>', testkey)
		test_to_post = q.get()

		title = self.request.get("title")
		privacy = self.request.get("privacy")

		# Create CommunityPostDB object from test
		newpost = CommunityPostDB(title=title,
								  author=user.nickname(),
								  test_ref=test_to_post,
								  privacy=privacy,
								  )
		newpost.put()

		self.redirect("/community")

class PrivateHandler(InstrumentDataHandler):
	def get (self):
        # Get all posts 
		posts = CommunityPostDB.all().order('-date_created')
		# Limit to just public posts
		posts.filter("privacy =", "private") 

		tests = TestDB.all()

		self.render('communitytests.html', posts=posts, tests=tests, counter=6)
