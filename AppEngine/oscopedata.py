from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import render_json
from gradientone import author_creation
from onedb import OscopeDB
from onedb import OscopeDB_key
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
    def get(self,name="",slicename=""):
        "retrieve Oscilloscope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'oscopedata' + name + slicename
        rows = memcache.get(key)
        if rows is None:
            logging.error("OscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                                AND slicename = :2""", name, slicename)  
            rows = list(rows)
            memcache.set(key, rows)
        data = query_to_dict(rows)
        output = {"data":data}
        render_json(self, output)
    def post(self,name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'oscopedata' + name + slicename
        oscope_content = json.loads(self.request.body)
        oscope_data = oscope_content['data']
        to_save = []
        for o in oscope_data:
            r = OscopeDB(parent = OscopeDB_key(name), name=name,
                         slicename=slicename,
                         config=str(oscope_content['config']),
                         data=(oscope_content['data']),
                         start_tse=(oscope_content['start_tse'])
                         )
        to_save.append(r) 
        memcache.set(key, to_save)
        db.put(to_save)