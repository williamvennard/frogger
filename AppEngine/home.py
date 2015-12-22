from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from gradientone import query_to_dict
from gradientone import convert_str_to_cha_list
from gradientone import get_ordered_list
from gradientone import co_and_tp_names
import itertools
import jinja2
import webapp2
import logging
import datetime
import settings
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
import json
from profile import get_profile_cookie


class Handler(InstrumentDataHandler):
    def get(self):
        profile = get_profile_cookie(self)
        instruments = ['U2000', 'Scope']
        ping = memcache.get('lastNUCping')
        if ping is None:
            ping = "No Recent Ping" 
        templatedata = {
            'hardware' : settings.HARDWARE,
            'software_version' : settings.SOFTWARE,
            'ping' : ping,
            'instruments' : instruments,
        }
        self.render('home.html', 
            data=templatedata, 
            profile=profile,
        )