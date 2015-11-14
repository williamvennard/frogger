from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import getKey
from gradientone import author_creation
from onedb import TestDB
from onedb import TestDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
import itertools
import jinja2
import json
import logging
import os
import re
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
import hashlib
from profile import get_profile_cookie


class Handler(InstrumentDataHandler):
    "Currently on the canvas page.  It presents to the user all of the completed tests, with a path that supports specific test entries"
    def get(self, company_nickname=""):
        user = users.get_current_user()
        if user:
            active_user = user.email()
            active_user= active_user.split('@')
            author = active_user[0]
            print author
        else:
            self.redirect(users.create_login_url(self.request.uri))
        profile = get_profile_cookie(self)
        company_nickname_check = company_nickname.split('.')
        company_nickname = company_nickname_check[0]
        if company_nickname_check[-1] == 'json':
            rows = db.GqlQuery("""SELECT * FROM ConfigDB WHERE company_nickname =:1""", company_nickname)
            configs = query_to_dict(rows)
            rows = db.GqlQuery("""SELECT * FROM DutDB WHERE company_nickname =:1""", company_nickname)
            duts = query_to_dict(rows)
            rows = db.GqlQuery("""SELECT * FROM MeasurementDB WHERE company_nickname =:1""", company_nickname)
            measurements = query_to_dict(rows)
            rows = db.GqlQuery("""SELECT * FROM TestDB WHERE company_nickname =:1""", company_nickname)
            tests = query_to_dict(rows)
            #rows = db.GqlQuery("""SELECT * FROM SequenceDB WHERE company_nickname =:1""", company_nickname)
            #sequences = query_to_dict(rows)
            widgets = {'tests':tests, 'measurements':measurements, 'configs':configs, 'duts':duts}
            render_json(self, widgets) 
        else:
            print 'just rendering the page'
            self.render('index.html', profile=profile)