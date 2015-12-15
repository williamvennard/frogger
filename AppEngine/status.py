from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import oauth_check
import jinja2
import json
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import oauth
import logging
import traceback


class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", hardware_name=""):
        key = 'status' + company_nickname + hardware_name
        status = memcache.get(key)
        render_json(self, status)
    def post(self, company_nickname="", hardware_name=""):
        status = json.loads(self.request.body)
        key = 'status' + company_nickname + hardware_name
        memcache.set(key, status)

class OAuthHandler(InstrumentDataHandler):
    def get(self, company_nickname="", hardware_name=""):
        oauth_check(self)
        key = 'status' + company_nickname + hardware_name
        status = memcache.get(key)
        render_json_cached(self, status)
