from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import getTestKey
from onedb import ConfigDB
from onedb import ConfigDB_key
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
    "An HTTP GET will present test plans.  Queries that include just company and hardware name are used to present instructions to the instrument for testing."
    def get(self, company_nickname="", hardware_name="", config_name=""):
        if company_nickname and hardware_name:
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_explore =:2 and hardware_name =:3 and config_name =:4", 
                                company_nickname, False, hardware_name, config_name)
            rows = list(rows)
            config_exps = query_to_dict(rows)
            config = {'configs_exps':config_exps}
            render_json(self, config)