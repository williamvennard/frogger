from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from measurements import root_mean_squared_ta
from measurements import peak_voltage_ta
from measurements import peak_to_peak_voltage_ta
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
    #work in progress.  To do:  modularize parsing and measurment calls.
    def get(self, instrument_name="", start_tse=""):
        print 'in the testanalyzer handler'
        key = 'bscopedata' + instrument_name + start_tse
        start_tse = int(start_tse)
        rows = memcache.get(key)
        if rows is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE instrument_name =:1
                            AND start_tse=:2 ORDER BY slicename ASC """, instrument_name, start_tse)  
            rows = list(rows)
            memcache.set(key, rows)
        data = query_to_dict(rows)
        config_settings = create_psettings(data[0]['p_settings'])
        start_time = 0 #miliseconds
        stop_time = config_settings['Total_Slices'] * config_settings['Slice_Size_msec'] * config_settings['Raw_msec_btw_samples']
        si = config_settings['Raw_msec_btw_samples']
        self.render('testanalyzer.html', test_sample = start_tse, start_time = start_time, stop_time = stop_time)        
    def post(self, instrument_name="", start_tse=""):
        key = 'bscopedata' + instrument_name + start_tse
        start_tse = int(start_tse)
        rows = memcache.get(key)
        if rows is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE instrument_name =:1
                                AND start_tse=:2 ORDER BY slicename ASC """, instrument_name, start_tse)  
            rows = list(rows)
            memcache.set(key, rows)
        data = query_to_dict(rows)
        config_settings = create_psettings(data[0]['p_settings'])
        start_time = 0 #miliseconds
        stop_time = config_settings['Total_Slices'] * config_settings['Slice_Size_msec'] * config_settings['Raw_msec_btw_samples']
        si = config_settings['Raw_msec_btw_samples']
        cha_list = convert_str_to_cha_list(data[0]['cha'])
        if self.request.get('measurement_RMS'):
            print 'RMS is checked'
            RMS_time_start = self.request.get('RMS_time_start')
            RMS_time_stop = self.request.get('RMS_time_stop')
            measurement_result = root_mean_squared_ta(cha_list, RMS_time_start, RMS_time_stop, si)
            print measurement_result
        elif self.request.get('measurement_peak_to_peak_voltage'):
            print 'p2p is checked'
            RMS_time_start = self.request.get('RMS_time_start')
            RMS_time_stop = self.request.get('RMS_time_stop')
            measurement_result = peak_to_peak_voltage_ta(cha_list, RMS_time_start, RMS_time_stop, si)
            print measurement_result
        elif self.request.get('peak_voltage'):
            print 'peak is checked'
            RMS_time_start = self.request.get('RMS_time_start')
            RMS_time_stop = self.request.get('RMS_time_stop')
            measurement_result = peak_voltage_ta(cha_list, RMS_time_start, RMS_time_stop, si)
            print measurement_result
        else:
            measurement_result = None
        self.render('testanalyzer.html', test_sample = start_tse, start_time = start_time, stop_time = stop_time, measurement_result = measurement_result)