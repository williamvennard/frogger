from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import author_creation
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import CommentsDB
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
from profile import get_profile_cookie

class Handler(InstrumentDataHandler):
    def get(self, company_nickname, testplan_name):
        profile = get_profile_cookie(self)
        if company_nickname and testplan_name:
            query = TestResultsDB.all().filter("company_nickname =", company_nickname)
            query = query.filter("testplan_name =", testplan_name)
            test_results = query.run()
            comment_thread = []
            logging.debug("TEST_RESULTS: %s" % test_results)
            # if test_results:
            #     comments_query = CommentsDB.all()
            #     comments_query.ancestor(test_results)
            #     comments = comments_query.run(limit=10)
            #     for comment in comments:
            #         comment_thread.append(comment)
            data = {
                'company_nickname' : company_nickname,
                'testplan_name' : testplan_name,
            }
            self.render('testLibResults.html', comment_thread=comment_thread, 
                data=data, profile = profile)
        else:
            logging.warn("Bad input for test results")
            self.redirect('/')


class JSON_Handler(InstrumentDataHandler):
    def get(self, company_nickname, testplan_name):
        rows = db.GqlQuery("""SELECT * FROM TestResultsDB 
                              WHERE testplan_name =:1
                              AND company_nickname =:2""",
                              testplan_name, 
                              company_nickname)
        test_results = query_to_dict(list(rows))
        render_json(self, test_results)