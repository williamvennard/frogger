from gradientone import InstrumentDataHandler
from gradientone import author_creation
from onedb import ConfigDB
from onedb import company_key
from onedb import ConfigDB_key
from onedb import agilentU2000
from onedb import agilentU2000_key
import itertools
import jinja2
import webapp2
from measurements import max_min
from measurements import threshold
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config

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
        author = 'nedwards'
        #author = author_creation()
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        config_name = self.request.get('config_name')
        trace_name = self.request.get('trace_name')
        averaging_count_auto= self.request.get('averaging_count_auto')
        correction_frequency = self.request.get('correction_frequency')
        offset = self.request.get('offset')
        range_auto = self.request.get('range_auto')
        units = self.request.get('units')
        testplan_name = self.request.get('trace_name')
        max_value = self.request.get('max_value')
        min_value = self.request.get('min_value')
        pass_fail = self.request.get('pass_fail')
        pass_fail_type = self.request.get('pass_fail_type')
        c = agilentU2000(key_name = (config_name+instrument_type), parent = company_key(),
            config_name = config_name,
            company_nickname = company_nickname, 
            hardware_name = hardware_name, 
            instrument_type = instrument_type,
            averaging_count_auto = averaging_count_auto, 
            correction_frequency = correction_frequency, 
            offset = offset, 
            range_auto = range_auto, 
            units = units,
            # max_value = max_value,
            # min_value = min_value,
            # pass_fail = pass_fail,
            # pass_fail_type = pass_fail_type,
            )
        c.put() 
        s = ConfigDB(key_name = config_name, parent = company_key(),
            config_name = config_name,
            company_nickname = company_nickname,
            hardware_name = hardware_name, 
            instrument_type = instrument_type,
            author = author,
            test_plan = False,
            active_testplan_name = testplan_name,
            trace = True,
            )
        s.put()

