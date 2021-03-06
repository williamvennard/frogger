from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import render_json_cached
from gradientone import unic_to_ascii
from gradientone import author_creation
from measurements import max_min
from measurements import threshold
from measurements import measurement_config
from onedb import company_key
from onedb import TestResultsDB
from onedb import TestResultsDB_key
from onedb import agilentU2000data
from onedb import agilentU2000data_key
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
    def get(self,company_nickname="", hardware_name="",config_name="",start_tse=""):
        "retrieve BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'u2000data' + company_nickname + hardware_name + config_name + start_tse
        cached_copy = memcache.get(key)
        if cached_copy is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE config_name =:1
                                AND slicename = :2""", config_name, slicename)  
            rows = list(rows)
            data = query_to_dict(rows)
            print data[0]
            cha_list = convert_str_to_cha_list(data[0]['cha'])
            data[0]['cha'] = cha_list
            e = data[0]
            print e
            print type(e)
            output = {"data":data[0]}
            output = json.dumps(e)
            memcache.set(key, output)
            render_json_cached(self, output)
        else:
            render_json_cached(self, cached_copy)



