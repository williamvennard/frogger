from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json_cached
from gradientone import author_creation
from gradientone import unic_to_ascii
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
    def post(self, company_nickname="", hardware_name="",config_name="",start_tse=""):
        key = 'u2000data' + company_nickname + hardware_name + config_name + start_tse
        u2000data = memcache.get(key)
        test_results_data = u2000data['cha']
        i_settings = u2000data['i_settings']
        a = agilentU2000data(parent = company_key(), key_name = start_tse,
                             config_name=config_name,
                             company_nickname = company_nickname,
                             hardware_name=hardware_name,
                             i_settings=str(i_settings),
                             test_results_data=str(test_results_data),
                             start_tse=int(start_tse)
                             )            
        a.put()