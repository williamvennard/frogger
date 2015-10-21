from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import render_json_cached
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import TestDB
from onedb import TestDB_key
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import company_key
from onedb import StateDB
import itertools
import jinja2
import json
import logging
import os
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
import datetime
from string import maketrans

class Handler(InstrumentDataHandler):
    def post(self, company_nickname="", config_name=""):
        key = config_name
        key = db.Key.from_path('ConfigDB', key, parent = company_key())
        config = db.get(key)
        config.commence_test = False
        config.put()