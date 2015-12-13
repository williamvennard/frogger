from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json_cached
from gradientone import author_creation
from gradientone import unic_to_ascii
from onedb import ConfigDB
from onedb import company_key
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
    def post(self, company_nickname="", hardware_name="",config_name="", testplan_name=""):
        control_object = json.loads(self.request.body)
        order = control_object['command']
        print order
        key_name = config_name
        # logging.debug("SWITCHING KEYNAME: %s" % key_name)
        key = db.Key.from_path('ConfigDB', key_name, parent = company_key())
        config = db.get(key)
        if order == 'Stop_Run':
            config.commence_run = False
        elif order == 'Start_Run':
            config.commence_run = True
            config.active_testplan_name = testplan_name
        elif order == 'Stop_Trace':
            config.commence_test = False
        elif order == 'Start_Trace':
            config.commence_test = True
            config.active_testplan_name = testplan_name
        config.put()






