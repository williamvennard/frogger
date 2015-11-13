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
    def get(self,company_nickname="", hardware_name="", config_name=""):
        "HTTP GETs from the Instrument Page in the UI provide data to faciliate plotting"
        #if not self.authcheck():
        #    return
        user = users.get_current_user()
        if user:
            active_user = user.email()
            active_user= active_user.split('@')
            author = active_user[0]
        else:
            self.redirect(users.create_login_url(self.request.uri))
        key = 'u2000_traceresultsdata' + company_nickname + hardware_name + config_name
        memcache.get(key)
        output = memcache.get(key)
        render_json_cached(self, output)
        #print company_nickname, hardware_name, config_name
        #rows = db.GqlQuery("""SELECT * FROM TestResultsDB WHERE company_nickname =:1 and hardware_name =:2
        #                        AND config_name = :3 and test_complete_bool =:4""", company_nickname, hardware_name, config_name, False)  
        #rows = list(rows)
        #data = query_to_dict(rows)
        #print data
        #output = {"data":data}
        #render_json(self, output)
    def post(self,company_nickname= "", hardware_name="", config_name = ""):
        "store data by intstrument name and time slice name"
        testresults_content = json.loads(self.request.body)
        test_plan = testresults_content['test_plan']
        if test_plan == 'True':
            testresults_content['test_plan'] = True
            testresults_content['trace'] = False
        else:
            testresults_content['test_plan'] = False
            testresults_content['trace'] = True
        testresults_content['test_complete_bool'] = False
        testresults_content = unic_to_ascii(testresults_content)
        key = 'u2000_traceresultsdata' + company_nickname + hardware_name + config_name
        testresults_output = json.dumps(testresults_content)
        memcache.set(key, testresults_output)
        i_settings = testresults_content['i_settings']
        start_tse = testresults_content['start_tse']
        cha = testresults_content['cha']
        testplan_name = testresults_content['testplan_name']
        window_u2000 = {'i_settings':i_settings, 'cha':cha, 'testplan_name':testplan_name,
        'start_tse':start_tse, 'company_nickname':company_nickname, 'hardware_name':hardware_name, 'config_name':config_name, 'test_plan':test_plan}
        out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
        key = 'u2000data' + company_nickname + hardware_name + config_name + str(start_tse)
        memcache.set(key, out_u2000)
