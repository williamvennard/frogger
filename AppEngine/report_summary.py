from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
# from gradientone import dt2ms
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
from onedb import Scope
from onedb import agilentBaseScope
from onedb import agilentBaseInfiniiVision
from onedb import agilent7000
from onedb import agilent7000A
from onedb import agilentMSO7014A
from onedb import agilentU2000data_key
from onedb import agilentU2000data
import jinja2
import json
import logging
import webapp2
import numpy
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import search
import appengine_config
from google.appengine.api import mail
from profile import get_profile_cookie
#from send_script_post import Script

DOMAIN = "gradientone-dev2.appspot.com"
INDEX_NAME = 'U2000'

class Handler(InstrumentDataHandler):
    def get(self, company_nickname=""):
        rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1", company_nickname)
        a = query_to_dict(rows)
        self.render('report_summary.html', rows = rows)
    def post(self, company_nickname=""):
        recipient_email = self.request.get('recipient_email')
        start_tse = self.request.get('start_tse')
        testplan_name = self.request.get('testplan_name')
        result_url = ('https://' + DOMAIN + '/testlibrary/testresults/' +
            company_nickname + '/' + testplan_name + '/' + start_tse)
        message = mail.EmailMessage(
            sender="GradientOne Support <nedwards@gradientone.com>",
            subject="Test Data For You!")
        message.to = recipient_email
        message.body = """

        John Doe has shared this link with you!

        """ + result_url + """

        GradientOne Inc
        """

        message.send()


def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)


class Selected(InstrumentDataHandler):
    def post(self):
        profile = get_profile_cookie(self)
        rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1", profile['company_nickname'])
        a = query_to_dict(rows)
        doc_ids = self.request.params.getall('doc_ids')
        try:
          index = search.Index(INDEX_NAME)
          selected_data = []
          for doc_id in doc_ids:
            fields = index.get(doc_id).fields
            for field in fields:
                if field.name == 'start_tse':
                    selected_data.append(field.value)
        except search.Error:
          logging.error("Search Results Error: %s" % e )
        logging.debug("Selected Configs: %s" % selected_data)

        keys = []
        for start in selected_data:
            keys.append(agilentU2000data_key(start))
        logging.debug("KEYS: %s" % keys)
        entities = db.get(keys)
        data = query_to_dict(entities)
        meas_results = []
        meas_results_calcs = []
        for entry in data:
            meas_results.append((float(entry['test_results_data']), entry['config_name'], entry['i_settings'])) 
            # meas_results.append((float(entry['test_results_data']), config_name, entry['i_settings'], ("https://gradientone-test.appspot.com/u2000data/" + company_nickname + '/' + entry['hardware_name'] +'/' + config_name + "/%s" % entry['start_tse'])))
            meas_results_calcs.append(float(entry['test_results_data']))
        mean_value = numpy.mean(meas_results_calcs)
        max_value = numpy.amax(meas_results_calcs)
        min_value = numpy.amin(meas_results_calcs)
        median_value = numpy.median(meas_results_calcs)
        std_value = numpy.std(meas_results_calcs)
        report_results = {'mean_value':mean_value, 'max_value':max_value, 'min_value':min_value, 'median_value':median_value, 'std_value':std_value, 'meas_results':meas_results}
        render_json(self, report_results)
        # self.render('report_summary.html', rows = rows, 
        #     selected_data=selected_data,
        #     profile=profile)
    
    def oldpost(self):
        profile = get_profile_cookie(self)
        rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1", profile['company_nickname'])
        a = query_to_dict(rows)
        doc_ids = self.request.params.getall('doc_ids')
        try:
          index = search.Index(INDEX_NAME)
          selected_configs = []
          for doc_id in doc_ids:
            fields = index.get(doc_id).fields
            for field in fields:
                if field.name == 'config_name':
                    selected_configs.append(field.value)
        except search.Error:
          logging.error("Search Results Error: %s" % e )
        logging.debug("Selected Configs: %s" % selected_configs)
        self.render('report_summary.html', rows = rows, 
            selected_data=selected_configs,
            profile=profile)
