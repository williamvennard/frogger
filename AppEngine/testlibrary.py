from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import UserDB
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
from profile import getProfile

class Handler(InstrumentDataHandler):
    def get(self, company_nickname=""):
<<<<<<< HEAD

        if company_nickname:
            company_nickname_check = company_nickname.split('.')
            company_nickname = company_nickname_check[0]
        if company_nickname and company_nickname_check[-1] == 'json':
            rows = db.GqlQuery("SELECT * FROM TestResultsDB where company_nickname =:1 and saved_state =:2", company_nickname, True) #saved data only
            rows = list(rows) 
            rows = query_to_dict(rows)        
            output = {} 
            output['results'] = rows 
            rows = db.GqlQuery("SELECT * FROM TestDB where company_nickname =:1", company_nickname)
            rows = list(rows)     
            rows = query_to_dict(rows)   
            output['test_configs'] = rows
            rows = db.GqlQuery("SELECT * FROM ConfigDB where company_nickname =:1", company_nickname)
            print rows
            rows = list(rows)     
            rows = query_to_dict(rows)   
            output['config_configs'] = rows
            render_json(self, output)
=======
        profile = getProfile()
        if hasattr(profile, 'company_nickname'):
            self.render('testlibrary.html', company_nickname=profile.company_nickname)
>>>>>>> refs/remotes/origin/master
        else:
            self.render('testlibrary.html', company_nickname=company_nickname)

class JSON_Handler(InstrumentDataHandler):
    def get(self, company_nickname=""):
        company_nickname_check = company_nickname.split('.')
        company_nickname = company_nickname_check[0]
        rows = db.GqlQuery("SELECT * FROM TestResultsDB where company_nickname =:1 and saved_state =:2", company_nickname, True) #saved data only
        rows = list(rows) 
        rows = query_to_dict(rows)        
        output = {} 
        output['results'] = rows 
        rows = db.GqlQuery("SELECT * FROM TestDB where company_nickname =:1", company_nickname)
        rows = list(rows)     
        rows = query_to_dict(rows)   
        output['test_configs'] = rows
        rows = db.GqlQuery("SELECT * FROM ConfigDB where company_nickname =:1", company_nickname)
        rows = list(rows)     
        rows = query_to_dict(rows)   
        output['config_configs'] = rows
        render_json(self, output)
