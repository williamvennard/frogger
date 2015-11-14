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
from onedb import CommentsDB


class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", config_name="", start_tse=""):
        if start_tse:
            start_tse_check = start_tse.split('.')
            start_tse = int(start_tse_check[0])
        if company_nickname and config_name and start_tse and start_tse_check[-1] == 'json':
            print "trace"
            rows = db.GqlQuery("SELECT * FROM TestResultsDB WHERE config_name =:1 and start_tse =:2 and company_nickname =:3", config_name, start_tse, company_nickname)
            rows = list(rows)            
            test_results = query_to_dict(rows)
            render_json(self, test_results)
        elif company_nickname and config_name and start_tse:
            query = TestResultsDB.all().filter("company_nickname =", company_nickname)
            query = query.filter("config_name =", config_name)
            query = query.filter("start_tse =", start_tse)
            test_results = query.get()
            comment_thread = []
            if test_results:
                comments_query = CommentsDB.all()
                comments_query.ancestor(test_results)
                comments = comments_query.run(limit=10)
                for comment in comments:
                    comment_thread.append(comment)

            data = {
                'company_nickname' : company_nickname,
                'config_name' : config_name,
                'start_tse' : start_tse,
            }
            self.render('testLibResults.html', comment_thread=comment_thread, data=data)
            

