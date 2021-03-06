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
        key = 'traceresults' + company_nickname + hardware_name + config_name
        output = memcache.get(key)
        if output == None:
            print 'DB Query'
            rows = db.GqlQuery("""SELECT * FROM TestResultsDB WHERE company_nickname =:1 and hardware_name =:2
                               AND config_name = :3 and test_complete_bool =:4""", company_nickname, hardware_name, config_name, False)  
            rows = list(rows)
            data = query_to_dict(rows)
            output = {"data":data}
            render_json(self, output)
        else:
            render_json(self, output)
    def post(self,company_nickname= "", hardware_name="", config_name = ""):
        "store data by intstrument name and time slice name"
        testresults_content = json.loads(self.request.body)
        print testresults_content
        i_settings = testresults_content['i_settings']
        cha = testresults_content['window_bscope']['cha']
        start_tse = testresults_content['start_tse']
        config_name=str(testresults_content['config_name'])
        test_plan = testresults_content['test_plan']
        if test_plan == 'True':
            testresults_content['test_plan'] = True
            testresults_content['trace'] = False
        else:
            testresults_content['test_plan'] = False
            testresults_content['trace'] = True
        testresults_content['test_complete_bool'] = False
        testresults_content['p_settings'] = unic_to_ascii(testresults_content['p_settings'])
        testresults_content['i_settings'] = unic_to_ascii(testresults_content['p_settings'])
        testresults_content['window_bscope'] = unic_to_ascii(testresults_content['window_bscope'])
        testresults_content = unic_to_ascii(testresults_content)
        render_json
        window_bscope = {'i_settings':i_settings, 'p_settings':testresults_content['p_settings'], 'cha':cha, 'start_tse':start_tse}
        window_bscope = json.dumps(window_bscope)
        key = 'bscopedatadec' + company_nickname + hardware_name + config_name + str(start_tse)
        memcache.set(key, window_bscope)
        key = 'traceresults' + company_nickname + hardware_name + config_name
        print testresults_content
        memcache.set(key, testresults_content)