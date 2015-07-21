from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import TestDB
from onedb import TestDB_key
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self,testplan_name=""):
        key = 'testplan_' + testplan_name 
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            memcache.set(key, configs)
        configs_out = [c.to_dict() for c in configs]
        render_json(self, configs_out)