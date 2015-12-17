from gradientone import InstrumentDataHandler
from gradientone import author_creation
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
import json
import itertools
import jinja2
import webapp2
import logging
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
from profile import get_profile_cookie


class Handler(InstrumentDataHandler):
    def get(self):
        #if not self.authcheck():
         #   return
        a = max_min(10.2, 2.3, 4.5)
        print a
        b = threshold(10.5, 4.5)
        print b
        self.render('u2000_configinput.html')
    def post(self):
        profile = get_profile_cookie(self)
        author = profile['name']
        #author = author_creation()
        config_data = json.loads(self.request.body)
        company_nickname = config_data['company_nickname']
        print company_nickname
        hardware_name = config_data['hardware_name']
        print hardware_name
        instrument_type = config_data['inst_name']
        config_name = config_data['config_name']
        trace_name = config_data['trace_name']
        averaging_count_auto= config_data['avg_count_auto']
        correction_frequency = config_data['correction_frequency']
        offset = config_data['offset']
        range_auto = config_data['range_auto']
        units = config_data['units']
        testplan_name = config_data['trace_name']
        # max_value = config_data['max_value']
        # min_value = config_data['min_value']
        # pass_fail = config_data['pass_fail']
        # pass_fail_type = config_data['pass_fail_type']
        measurement = ""
        if config_data.has_key('measurement'):
            measurement = config_data['measurement']
        logging.debug("range auto: % s" % range_auto)
        logging.debug("averaging count auto: %s" % averaging_count_auto)
        c = agilentU2000(key_name = config_name+instrument_type, parent = company_key(),
            config_name = config_name,
            company_nickname = company_nickname, 
            hardware_name = hardware_name, 
            instrument_type = instrument_type,
            averaging_count_auto = bool(averaging_count_auto), 
            correction_frequency = correction_frequency, 
            offset = offset, 
            range_auto = bool(range_auto), 
            units = units,
            # max_value = max_value,
            # min_value = min_value,
            # pass_fail = pass_fail,
            pass_fail_type = 'N/A',
            test_plan = False,
            )
        c.put() 
        s = ConfigDB(key_name = config_name, parent = company_key(),
            config_name = config_name,
            company_nickname = company_nickname,
            hardware_name = hardware_name, 
            instrument_type = instrument_type,
            measurement = measurement,
            author = author,
            test_plan = False,
            active_testplan_name = testplan_name,
            trace = True,
            )
        s.put()

