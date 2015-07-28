from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
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
    def get(self, company_nickname="", testplan_name="", start_tse=""):
        if company_nickname:
            company_nickname_check = company_nickname.split('.')
            company_nickname = company_nickname_check[0]
        if start_tse:
            start_tse_check = start_tse.split('.')
            start_tse = int(start_tse_check[0])
        if company_nickname and testplan_name and start_tse and start_tse_check[-1] == 'json':
            rows = db.GqlQuery("SELECT * FROM TestResultsDB WHERE testplan_name =:1 and start_tse =:2 and company_nickname =:3", testplan_name, start_tse, company_nickname)
            rows = list(rows)            
            test_results = query_to_dict(rows)
            render_json(self, test_results)
        elif company_nickname and testplan_name and start_tse:
            self.render('testLibResults.html')
        elif company_nickname and company_nickname_check[-1] == 'json':
            rows = db.GqlQuery("SELECT * FROM TestResultsDB where company_nickname =:1", company_nickname)
            rows = list(rows) 
            rows = query_to_dict(rows)        
            output = {}
            output['results'] = rows 
            rows = db.GqlQuery("SELECT * FROM TestDB where company_nickname =:1", company_nickname)
            rows = list(rows)     
            rows = query_to_dict(rows)   
            output['configs'] = rows
            render_json(self, output)
        else:
            self.render('testlibrary.html')