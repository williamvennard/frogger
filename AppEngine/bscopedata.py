from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json_cached
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
    def get(self,company_nickname="", hardware_name="",instrument_name="",slicename=""):
        "retrieve BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'bscopedata' + company_nickname + hardware_name + instrument_name + slicename
        cached_copy = memcache.get(key)
        if cached_copy is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE instrument_name =:1
                                AND slicename = :2""", instrument_name, slicename)  
            rows = list(rows)
            data = query_to_dict(rows)
            cha_list = convert_str_to_cha_list(data[0]['cha'])
            data[0]['cha'] = cha_list
            output = {"data":data}
            output = json.dumps(output)
            memcache.set(key, output)
            render_json_cached(self, output)
        else:
            render_json_cached(self, cached_copy)
    def post(self,company_nickname="", hardware_name="", instrument_name="",start_tse=""):
        "store data by intstrument name and time slice name"
        key = 'bscopedata' + company_nickname + hardware_name + instrument_name + start_tse
        memcache.set(key, self.request.body)
        test_results = json.loads(self.request.body)
        test_results_data = test_results['cha']
        data_length = len(test_results_data)
        slice_size = int(test_results['p_settings']['Slice_Size_msec'])
        sample_rate = int(test_results['i_settings']['Sample_Rate_Hz'])
        sample_per_slice = int((float(sample_rate)/1000)*float(slice_size))
        stuffing = []
        for i in range(0, data_length, sample_per_slice):
            chunk = str(test_results_data[i:i + sample_per_slice])
            slicename = int(start_tse) + i
            stuffing = chunk
            key = 'bscopedata' + company_nickname + hardware_name + instrument_name + str(slicename)
            window_bscope = {'i_settings':test_results['i_settings'], 'p_settings':test_results['p_settings'], 'cha':stuffing, 
            'start_tse':start_tse, 'company_nickname':company_nickname, 'slicename':slicename, 'hardware_name':hardware_name, 'instrument_name':instrument_name}
            out_bscope = json.dumps(window_bscope, ensure_ascii=True)
            print out_bscope
            memcache.set(key, out_bscope)