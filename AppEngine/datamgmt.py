from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json_cached
from gradientone import author_creation
from gradientone import unic_to_ascii
from onedb import BscopeDB
from onedb import company_key
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
    def post(self, company_nickname="", hardware_name="",config_name="",start_tse=""):
        save = self.request.body
        print save
        save_object = json.loads(self.request.body)
        print save_object
        save_status = save_object['save_status']
        slice_count = save_object['totalNumPages']
        Slice_Size_msec = save_object['sliceSize']
        check_slices = 0
        slicename = start_tse
        for s in range(0, slice_count):
            key = 'bscopedata' + company_nickname + hardware_name + config_name + slicename
            bscope_content = memcache.get(key)
            bscope_content = json.loads(bscope_content)
            original_p = bscope_content['p_settings']
            original_i = bscope_content['i_settings']
            new_p = unic_to_ascii(original_p)
            new_i = unic_to_ascii(original_i)
            to_save = []
            r = BscopeDB(parent = company_key(), key_name = slicename,
                            config_name=config_name,
                             company_nickname = company_nickname,
                             hardware_name= hardware_name,
                             slicename=(slicename),
                             p_settings=str(new_p),
                             i_settings=str(new_i),
                             cha=str((bscope_content['cha'])),
                             start_tse=int(bscope_content['start_tse'])
                             )
            to_save.append(r) 
            db.put(to_save)
            check_slices += 1
            slicename = int(slicename)
            slicename += int(Slice_Size_msec)
            slicename = str(slicename)
        if check_slices == slice_count:
            print check_slices, "Successfully saved."
            if trace == True:
                key_name = config_name + testplan_name
                key = db.Key.from_path('TestResultsDB', key_name, parent = company_key())
                configuration = db.get(key)
                configuration.saved_state = True
                configuration.put()
        else:
            print "Error:", check_slices, "saved.  The server was expecting to save:", slice_count