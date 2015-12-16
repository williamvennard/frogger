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

def parseisettings(i_settings):
    i_list = []
    a = str(i_settings)
    print a
    b = a.split(',')
    b1 = b[0].split(':')
    b1 = str(b1[1].strip().lstrip('u'))
    b1 = b1.strip("'")
    i_list.append(b1) #appending pass_fail_type
    for i in b[1:-1]:
        new_i = i.split(':')
        new_i = str(new_i[-1])
        new_i = new_i.strip()
        new_i = new_i.strip("u'")
        print new_i
        new_i = float(new_i)
        i_list.append(new_i)
    bn1 = b[-1].split(':')
    bn1 = str(bn1[-1].strip().lstrip('u').rstrip('}')) # pass_fail
    bn1 = bn1.strip("'")
    i_list.append(bn1)
    return i_list


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
            i_list = parseisettings(entry['i_settings'])
            i_list.insert(0, str(entry['config_name']))
            i_list.insert(1, float(entry['test_results_data']))
            meas_results.append(i_list)
            # meas_results.append((float(entry['test_results_data']), entry['config_name'], i_list)) 
            # meas_results.append((float(entry['test_results_data']), config_name, entry['i_settings'], ("https://gradientone-test.appspot.com/u2000data/" + company_nickname + '/' + entry['hardware_name'] +'/' + config_name + "/%s" % entry['start_tse'])))
            meas_results_calcs.append(float(entry['test_results_data']))
        print meas_results
        stat_results = []
        stat_results.append(numpy.amax(meas_results_calcs)) #max value
        stat_results.append(numpy.amin(meas_results_calcs)) #min value
        stat_results.append(numpy.median(meas_results_calcs)) #median 
        stat_results.append(numpy.mean(meas_results_calcs)) #mean 
        stat_results.append(numpy.std(meas_results_calcs)) #standard deviation 
        temp_list = []
        self.render('report_detail.html', stat_results = stat_results, meas_results = meas_results, profile = profile)


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
