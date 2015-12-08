from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import company_key
from onedb import CommentsDB
from onedb import TestResultsDB
import datetime
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.ext import db
from profile import get_profile_cookie


class Handler(InstrumentDataHandler):
    def post(self):
        """posts a comment on the test results"""
        profile = get_profile_cookie(self)
        if (not profile) or (profile['permissions'] == 'viewer'):
            self.redirect('/profile')
        data = json.loads(self.request.body)
        testplan_name = data['testplan_name']
        start_tse = data['start_tse']
        content = data['content']
        author = data['author']
        comment_time = data['comment_time']
        key_name = testplan_name+str(start_tse)
        key = db.Key.from_path('TestResultsDB', key_name, parent = company_key())
        test_results = TestResultsDB.get(key)
        comment = CommentsDB(author=author, content=content, parent=test_results)
        comment.put()
        templatedata = {}
        comment_thread = {}
        comment_thread['content'] = content
        comment_thread['author'] = author
        comment_thread['timestamp'] = datetime.datetime.now()
        templatedata['comment_thread'] = comment_thread
        print templatedata