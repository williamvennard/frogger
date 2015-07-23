from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import render_json_cached
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
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
    def get(self,company_nickname="", hardware_name="", instrument_name=""):
        "HTTP GETs from the Instrument Page in the UI provide data to faciliate plotting"
        #if not self.authcheck():
        #    return
        key = 'testresults' + hardware_name + instrument_name
        memcache.get(key)
        output = memcache.get(key)
        render_json_cached(self, output)
        #rows = db.GqlQuery("""SELECT * FROM TestResultsDB WHERE company_nickname =:1 and hardware_name =:2
        #                        AND instrument_name = :3 and test_complete_bool =:4""", company_nickname, hardware_name, instrument_name, False)  
        #rows = list(rows)
        #data = query_to_dict(rows)
        #output = {"data":data}
        #render_json(self, output)
    def post(self,company_nickname= "", testplan_name="",start_tse=""):
        "store data by intstrument name and time slice name"
        testresults_content = json.loads(self.request.body)
        instrument_name=str(testresults_content['instrument_name'])
        hardware_name=str(testresults_content['hardware_name'])
        test_plan = testresults_content['test_plan']
        if test_plan == 'True':
            testresults_content['test_plan'] = True
            testresults_content['trace'] = False
        else:
            testresults_content['test_plan'] = False
            testresults_content['trace'] = True
        testresults_content['test_complete_bool'] = False
        testresults_content['p_settings'] = unic_to_ascii(testresults_content['p_settings'])
        testresults_content = unic_to_ascii(testresults_content)
        key = 'testresults' + hardware_name + instrument_name
        testresults_content = json.dumps(testresults_content)
        print testresults_content
        memcache.set(key, testresults_content)