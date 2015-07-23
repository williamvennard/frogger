from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import render_json_cached
from measurements import create_decimation
from gradientone import author_creation
from onedb import BscopeDB
from onedb import BscopeDB_key
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
    def get(self,company_nickname="", hardware_name="",instrument_name="",start_tse=""):
        "retrieve decimated BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'bscopedatadec' + company_nickname + hardware_name + instrument_name + start_tse
        start_tse = int(start_tse)
        bscope_payload = memcache.get(key)
        print bscope_payload
        if bscope_payload is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE company_nickname =:1 and hardware_name =:2 and instrument_name =:3 AND start_tse= :4 ORDER BY slicename ASC""", company_nickname, hardware_name, instrument_name, start_tse)  
            rows = list(rows)
            data = query_to_dict(rows)
            test_results = create_decimation(data)
            bscope_payload = {'i_settings':data[0]['i_settings'], 'p_settings':data[0]['p_settings'] ,'slicename':data[0]['slicename'],'cha':test_results, 'start_tse':data[0]['start_tse']}
            memcache.set(key, bscope_payload)
            render_json(self, bscope_payload)
        else:
            if type(bscope_payload) == str:
                render_json_cached(self, bscope_payload)
            else:
                render_json(self, bscope_payload)
    def post(self,company_nickname="", hardware_name="", instrument_name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'bscopedatadec' + company_nickname + hardware_name + instrument_name + slicename
        print self.request.body
        memcache.set(key, self.request.body)