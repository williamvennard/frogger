from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import getTestKey
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import agilentU2000
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
from collections import defaultdict
from gradientone import oauth_check

class Handler(InstrumentDataHandler):
    "An HTTP GET will present test plans.  Queries that include just company and hardware name are used to present instructions to the instrument for testing."
    def get(self, company_nickname="", hardware_name="", testplan_name=""):
        if not oauth_check(self):
            return
        if company_nickname and hardware_name and testplan_name:
            rows = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", 
                                company_nickname, testplan_name)
            test_config = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname = :1 and hardware_name =:2 and testplan_name =:3", 
                                company_nickname, hardware_name, testplan_name)
            inst_config = query_to_dict(rows)
            config = {'test_config':test_config, 'inst_config':inst_config}
            render_json(self, config)
        elif company_nickname and hardware_name:
            commands = ["keep doing what you are doing", "say cheese!"]
            # grab configs set to commence
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_test =:2 and hardware_name =:3", 
                                company_nickname, True, hardware_name)
            rows = list(rows)
            configs_tps_traces = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_run =:2 and hardware_name =:3", 
                                company_nickname, True, hardware_name)
            rows = list(rows)
            configs_run = query_to_dict(rows)
            # grab instrument configurations associated with the config that need to run
            if configs_tps_traces:
                logging.debug("CONFIG_TPS_TRACES %s", configs_tps_traces)
                nested_config_name = configs_tps_traces[0]['config_name']
                nested_instrument_type = configs_tps_traces[0]['instrument_type']
                rows = db.GqlQuery("SELECT * FROM agilentU2000 WHERE company_nickname =:1 and config_name =:2", 
                                    company_nickname, nested_config_name)
                nested_config = query_to_dict(rows)
                logging.debug("NESTED_CONFIG %s", nested_config)
                # grab measurements associated with the config
                rows = db.GqlQuery("SELECT * FROM MeasurementDB WHERE company_nickname =:1 and config_name =:2",
                                    company_nickname, nested_config_name)
                measurements = query_to_dict(rows)
                rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_explore =:2 and hardware_name =:3", 
                                    company_nickname, True, hardware_name)
                rows = list(rows)
                configs_exps = query_to_dict(rows)
                rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_run =:2 and hardware_name =:3", 
                                company_nickname, True, hardware_name)
                rows = list(rows)
                configs_run = query_to_dict(rows)
                config = {
                            'configs_exps' : configs_exps, 
                            'configs_tps_traces' : configs_tps_traces, 
                            'configs_run' : configs_run,
                            'nested_config' : nested_config,
                            'measurements' : measurements,
                            'commands' : commands,
                }
            elif configs_run:
                logging.debug("CONFIG_TPS_TRACES %s", configs_tps_traces)
                nested_config_name = configs_tps_traces[0]['config_name']
                nested_instrument_type = configs_tps_traces[0]['instrument_type']
                rows = db.GqlQuery("SELECT * FROM agilentU2000 WHERE company_nickname =:1 and config_name =:2", 
                                    company_nickname, nested_config_name)
                nested_config = query_to_dict(rows)
                logging.debug("NESTED_CONFIG %s", nested_config)
                # grab measurements associated with the config
                rows = db.GqlQuery("SELECT * FROM MeasurementDB WHERE company_nickname =:1 and config_name =:2",
                                    company_nickname, nested_config_name)
                measurements = query_to_dict(rows)
                rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_explore =:2 and hardware_name =:3", 
                                    company_nickname, True, hardware_name)
                rows = list(rows)
                configs_exps = query_to_dict(rows)
                rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1 and commence_run =:2 and hardware_name =:3", 
                                company_nickname, True, hardware_name)
                rows = list(rows)
                configs_run = query_to_dict(rows)
                config = {
                            'configs_exps' : configs_exps, 
                            'configs_tps_traces' : configs_tps_traces, 
                            'configs_run' : configs_run,
                            'nested_config' : nested_config,
                            'measurements' : measurements,
                            'commands' : commands,
                }
            else:
                config = {
                            'configs_tps_traces' : None,
                            'commands' : commands,
                }
            render_json(self, config)