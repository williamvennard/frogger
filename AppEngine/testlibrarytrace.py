from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import company_key
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
from onedb import CommentsDB
from profile import get_profile_cookie

class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", config_name="", start_tse=""):
        profile = get_profile_cookie(self)
        if start_tse:
            start_tse_check = start_tse.split('.')
            start_tse = int(start_tse_check[0])
        if company_nickname and config_name and start_tse and start_tse_check[-1] == 'json':
            print "trace"
            rows = db.GqlQuery("""SELECT * FROM TestResultsDB 
                WHERE config_name =:1 AND start_tse =:2 
                AND company_nickname =:3""", 
                config_name, start_tse, company_nickname)
            rows = list(rows)            
            test_results = query_to_dict(rows)
            render_json(self, test_results)
        elif company_nickname and config_name and start_tse:
            query = TestResultsDB.all().filter("company_nickname =", company_nickname)
            query = query.filter("config_name =", config_name)
            query = query.filter("start_tse =", start_tse)
            test_results = query.get()
            comment_thread = []
            testplan_name = ""
            if test_results:
                testplan_name = test_results.testplan_name
                comments_query = CommentsDB.all()
                comments_query.ancestor(test_results)
                comments = comments_query.run(limit=10)
                for comment in comments:
                    comment_thread.append(comment)

            data = {
                'company_nickname' : company_nickname,
                'config_name' : config_name,
                'start_tse' : start_tse,
                'testplan_name' : testplan_name,
            }
            self.render('testLibResults.html', comment_thread=comment_thread, 
                data=data, profile = profile)

    def post(self, company_nickname="", config_name="", start_tse=""):
        """posts a comment on the test results"""
        profile = get_profile_cookie(self)
        author = profile['name']
        content = self.request.get('content')
        testplan_name = self.request.get('testplan_name')
        key_name = testplan_name+str(start_tse)
        print "key_name", key_name
        key = db.Key.from_path('TestResultsDB', key_name, parent = company_key())
        test_results = TestResultsDB.get(key)
        comment = CommentsDB(author=author, content=content, parent=test_results)
        comment.put()
        self.redirect('/testlibrary/traceresults/' + company_nickname + '/' + config_name + '/'
                        + start_tse)
            

