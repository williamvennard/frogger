from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import getKey
from gradientone import author_creation
from onedb import TestDB
from onedb import TestDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
import itertools
import jinja2
import json
import logging
import os
import re
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config

class Handler(InstrumentDataHandler):
    "Currently on the canvas page.  It presents to the user all of the completed tests, with a path that supports specific test entries"
    def get(self, testplan_name="", name="", slicename=""):
        #if not self.authcheck():
        #    return
        author = author_creation()
        testplan_name_check = testplan_name.split('.')
        testplan_name = testplan_name_check[0]
        key = 'oscope' + testplan_name
        name = 'LED'
        slicename = str(1435107043000)
        data_key = 'oscopedata' + name + slicename
        if testplan_name_check[-1] == 'json':
            rows = memcache.get(data_key)
            if rows is None:
                logging.error("OscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                    AND slicename = :2 ORDER BY DTE ASC""", name, slicename)
                rows = list(rows)
                rows = sorted(rows, key=getKey)
            memcache.set(data_key, rows)
            test_data = [r.to_dict() for r in rows]  
            test = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            test = [t.to_dict() for t in test]
            test_result = {"data":test_data, "test_config":test} 
            render_json(self, test_result) 
        elif testplan_name:
            f = open(os.path.join('templates', 'testResultsPage.html'))
            self.response.write((f.read()))
        else:
            tests = db.GqlQuery("SELECT * FROM TestDB")
            rows = memcache.get(key)
            print "hi"
            if rows is None:
                logging.error("OscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                    AND slicename = :2 ORDER BY DTE ASC""", name, slicename)
                rows = list(rows)
                rows = sorted(rows, key=getKey)
            memcache.set(data_key, rows)
            self.render('index.html', tests = tests, rows = rows)