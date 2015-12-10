from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import render_json_cached
from gradientone import query_to_dict
from gradientone import convert_str_to_cha_list
from gradientone import get_ordered_list
from gradientone import co_and_tp_names
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000data
from onedb import agilentU2000_key
from onedb import TestInterface
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import CommentsDB
from onedb import TestDB
from onedb import StateDB
from onedb import TestResultsDB
import itertools
import jinja2
import webapp2
import logging
import datetime
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
import json
from profile import get_profile


class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", hardware_name="", testplan_name=""):
        comp_cookie = self.request.cookies.get("company_nickname")
        if comp_cookie:
            profile = {}
            profile['company_nickname'] = comp_cookie
        else:
            profile = get_profile()

        templatedata = {
                'company_nickname' : company_nickname,
                'hardware_name' : hardware_name,
                'testplan_name' : testplan_name,
                }

        query = TestDB.all().filter("company_nickname =", company_nickname)
        query = query.filter("testplan_name =", testplan_name)
        testplan = query.get()
        comment_thread = []
        if testplan:
            templatedata['testplan'] = testplan.to_dict()
            measurements = []
            for m_key in testplan.measurements:
                measurements.append(db.get(m_key).to_dict())
            templatedata['measurements'] = measurements
            configs = []
            for c_key in testplan.configs:
                configs.append(db.get(c_key).to_dict())
            templatedata['configs'] = configs
            comments_query = CommentsDB.all()
            comments_query.ancestor(testplan)
            comments = comments_query.run(limit=10)
            for comment in comments:
                comment_thread.append(comment)

        templatedata['comment_thread'] = comment_thread
        self.render('view_testplan.html', data=templatedata, profile=profile)


    def post(self, company_nickname="", hardware_name="", testplan_name=""):
        """posts a comment on the test results"""
        user = users.get_current_user()
        if not user.nickname():
            author = "anonymous"
        else:
            author = user.nickname()
        content = self.request.get('content')
        key_name = testplan_name
        key = db.Key.from_path('TestDB', key_name, parent = company_key())
        test = TestDB.get(key)
        comment = CommentsDB(author=author, content=content, parent=test)
        comment.put()
        self.redirect('/view_testplan/' + company_nickname + '/' + hardware_name + '/'
                        + testplan_name)


