from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from gradientone import query_to_dict
from gradientone import get_ordered_list
from gradientone import co_and_tp_names
from onedb import ConfigDB
from onedb import company_key
from onedb import TestDB
from onedb import DutDB
from onedb import CapabilitiesDB
from onedb import InstrumentsDB
from onedb import StateDB
import datetime
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
#from odermanager import OrderManager


class Handler(InstrumentDataHandler):
    def post(self):
        print self.request.body
        names = co_and_tp_names(self.request.body)
        results = db.GqlQuery("SELECT configs FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", names[0], names[-1])
        for r in results:
            config = db.get(r.configs[0])
            config_dict = {}
            config_dict['company_nickname'] = config.company_nickname
            config_dict['config_name'] = config.config_name
            config_dict['hardware_name'] = config.hardware_name
            config_dict['instrument_type'] = config.instrument_type
            config_dict['capture_buffer_size'] = config.capture_buffer_size
        results = db.GqlQuery("SELECT * FROM TestDB WHERE company_nickname =:1 and testplan_name =:2", names[0], names[-1])
        test_dict = [c.to_dict() for c in results]
        print test_dict
        order = str(test_dict[0]['order'])
        order_list = get_ordered_list(order)
        for o in order_list:
            op = StateDB(key_name = (names[-1]+o['type']+o['name']), parent = company_key(),
                    testplan_name = names[-1],
                    company_nickname = names[0],
                    widget = o['type'],
                    name = o['name'],
                    order = int(o['order']),
                    )
            op.put()
        first_event = ConfigDB.gql("Where config_name =:1", order_list[0]['name']).get()
        print order_list[0]
        print first_event
        first_event.commence_test = True
        first_event.active_testplan_name = names[-1]
        first_event.put()
        start_time = datetime.datetime.now()
        key = db.Key.from_path('TestDB', names[-1], parent = company_key())
        testplan = db.get(key)
        testplan.start_time = start_time
        testplan.put()
        first_key = names[-1]+order_list[0]['type']+order_list[0]['name']
        key = db.Key.from_path('StateDB', first_key, parent = company_key())
        state_first_event = db.get(key)
        state_first_event.start_time = start_time
        state_first_event.put()


