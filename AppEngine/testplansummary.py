from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import getTestKey
from onedb import ConfigDB
from onedb import ConfigDB_key
import ast
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
    "An HTTP GET will present test plans.  Queries that include just company and hardware name are used to present instructions to the instrument for testing."
    def get(self, company_nickname="", hardware_name="", testplan_name=""):
        if company_nickname and hardware_name and testplan_name:
            rows = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", 
                                company_nickname, testplan_name)
            test_config = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname = :1 and hardware_name =:2 and testplan_name =:3", 
                                company_nickname, hardware_name, testplan_name)
            inst_config = query_to_dict(rows)
            config = {'test_config':test_config, 'inst_config':inst_config}
            render_json(self, config)
        elif company_nickname and hardware_name:
            configs = []
            rows = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and commence_test =:2", 
                              company_nickname, True)
            rows = list(rows)            
            test_config = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and test_plan =:2 and hardware_name =:3", 
                                company_nickname, True, hardware_name)
            rows = list(rows)
            inst_config = query_to_dict(rows)
            for t in test_config:
                for i in inst_config: 
                    if i['testplan_name'] == t['testplan_name']:
                        t['inst_config'] = i
            for t in test_config:
                configs.append(t)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_test =:2 and hardware_name =:3", 
                    company_nickname, True, hardware_name)
            rows = list(rows)
            meas_config = query_to_dict(rows)
            for m in meas_config:
                configs.append(m)
            config_list = sorted(configs, key=getTestKey)
            config = {'configs':config_list}
            render_json(self, config)