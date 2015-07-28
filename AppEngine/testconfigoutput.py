from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from onedb import TestDB
from onedb import TestDB_key
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self,company_nickname="",testplan_name=""):
        #key = 'testplan_' + company_nickname + testplan_name 
        #configs = memcache.get(key)
        #if configs is None :
        #logging.error("DB Query")
        results = db.GqlQuery("SELECT configs FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", company_nickname, testplan_name)
            #memcache.set(key, configs)

        for c in results:
            print c.configs[0]
            print type(c.configs[0])
            who = db.get(c.configs[0])
            print who
        config_dict = {}
        config_dict['company_nickname'] = who.company_nickname
        config_dict['config_name'] = who.config_name
        config_dict['hardware_name'] = who.hardware_name
        config_dict['instrument_type'] = who.instrument_type
        config_dict['number_of_samples'] = who.number_of_samples
        print config_dict
        test_dict = [c.to_dict() for c in results]
        #print configs_dict
        #dut_key = str(configs_dict[0]['duts'])
        #print dut_key
        #dut_key = (dut_key.lstrip('[').rstrip(']'))
        #print dut_key
        #print type(dut_key)
        #dut = db.get(dut_key)
        render_json(self, test_dict)