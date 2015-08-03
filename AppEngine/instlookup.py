from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import render_json_cached
from gradientone import author_creation
from gradientone import query_to_dict
from gradientone import is_checked
from gradientone import instruments_and_explanations
from onedb import ConfigDB
from onedb import company_key
from onedb import TestDB
from onedb import DutDB
from onedb import CapabilitiesDB
from onedb import InstrumentsDB
from onedb import MeasurementDB
from datetime import datetime
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import taskqueue
import appengine_config


class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", testplan_name=""):
        key = 'instlookup' + company_nickname + testplan_name
        result = memcache.get(key)
        render_json_cached(self, result)

    def post(self, company_nickname="", testplan_name=""):
        inst_object = json.loads(self.request.body)
        print inst_object
        analog_bandwidth = inst_object['analog_bandwidth']
        analog_sample_rate = inst_object['analog_sample_rate']
        capture_buffer_size = inst_object['capture_buffer_size']
        capture_channels = inst_object['capture_channels']
        resolution = inst_object['resolution']
        insts_and_explanations = instruments_and_explanations(analog_bandwidth, analog_sample_rate, capture_buffer_size, capture_channels, resolution)
        instruments = insts_and_explanations[0]
        explanations = insts_and_explanations[-1]
        avail = []
        for inst in instruments:
            i = InstrumentsDB.gql("Where instrument_type =:1", inst)
            for entry in i:
                avail.append((inst, entry.hardware_name))
        if len(avail) == 0:
            selected_inst_type = "None Selected"
            selected_hardware = "None Selected"
            avail = "None available"
        else:
            selected_inst_type = avail[0][0]
            selected_hardware = avail[0][1]
            avail = avail
        results = {'explanations':explanations, 'selected_inst_type':selected_inst_type, 'selected_hardware':selected_hardware, 'avail_inst':avail}
        results = json.dumps(results, ensure_ascii=True)
        key = 'instlookup' + company_nickname + testplan_name
        memcache.set(key, results)
            
