from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import dropdown_creation
from gradientone import author_creation
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import TestResultsDB
from onedb import TestResultsDB_key
import itertools
import jinja2
import json
import logging
import os
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self, name="", slicename="", start_tse=""):
        dropdown = dropdown_creation()
        self.render('search.html', dropdown = dropdown)
    def post(self):
        dropdown = dropdown_creation()
        name = self.request.get('name')
        if int(self.request.get('start_time')):
            start_time = int(self.request.get('start_time'))
        else:
            start_time = None
        end_time = int(self.request.get('end_time'))
        instrument = self.request.get('instrument')
        testplan_name = self.request.get('testplan_name')
        if instrument == 'BitScope':
            instrument = BscopeDB.gql
        elif instrument == 'Tektronix':
            instrument = OscopeDB.gql
        #query = instrument("where name = :1 and start_tse =:2 and slicename =:3 and config =:4", name, start_tse, slicename, config)
        results = set()
               #summary.add((str(r.start_tse), str(r.name), str(r.config))) #make set to eliminate dupes
        query=TestResultsDB.all()
        start_tse_query = query.filter("start_tse =",start_time).run()
        for i in start_tse_query:
            results.add((str(i.start_tse), str(i.name)))
        #config_query = query.filter("config =",config).run()
        #for i in config_query:
            #results.add((str(i.start_tse), str(i.name)))
        #results = list(results)
        self.render('search.html', results = results, dropdown = dropdown, name = name, slicename = slicename, start_time = start_time, end_time = end_time)