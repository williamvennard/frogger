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
import collections
from datetime import datetime
import StringIO
import csv

DOMAIN = "gradientone-test.appspot.com"
INDEX_NAME = 'U2000'

def dt2ms(t):
    return str(t.strftime('%s'))*1000 + str(t.microsecond/1000)

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
    b = a.split(',')
    b1 = b[0].split(':')
    b1 = str(b1[1].strip().lstrip('u'))
    b1 = b1.strip("'")
    i_list.append(b1) #appending pass_fail_type
    for i in b[1:4]: #appends max, min, and offset
        new_i = i.split(':')
        new_i = str(new_i[-1])
        new_i = new_i.strip()
        new_i = new_i.strip("u'")
        new_i = float(new_i)
        i_list.append(new_i)
    bn4 = b[-4].split(':')
    bn4 = str(bn4[-1])
    bn4 = bn4.strip()
    bn4 = bn4.strip("u'")
    i_list.append(bn4) # appends test_plan
    bn3 = b[-3].split(':') 
    bn3 = str(bn3[-1])
    bn3 = bn3.strip()
    bn3 = bn3.strip("u'")
    i_list.append(bn3)    #appends correction freq
    bn2 = b[-2].split(':')
    bn2 = str(bn2[-1])
    bn2 = bn2.strip()
    bn2 = bn2.strip("u'")
    i_list.append(bn2)  # appends  active testplan name
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
            print i_list
            temp_i_list = []
            temp_i_list.insert(0, str(entry['start_tse']))
            temp_i_list.insert(1, i_list[5]) #+1
            temp_i_list.insert(2, i_list[1]) #+2
            temp_i_list.insert(3, i_list[2]) #+3
            temp_i_list.insert(4, i_list[3]) #+4
            temp_i_list.insert(5, i_list[0])  #+5
            temp_i_list.insert(6, i_list[4]) #+6
            temp_i_list.insert(7, i_list[-1])
            temp_i_list.insert(8, (entry['hardware_name'])) #+7
            temp_i_list.insert(9, float(entry['test_results_data'])) #+8
            temp_i_list.insert(10, 'U2001') #+9
            temp_i_list.insert(11, str(entry['config_name'])) #+10
            temp_i_list.insert(12, i_list[6]) #+11
            meas_results.append(temp_i_list)
            meas_results_calcs.append(float(entry['test_results_data']))
        stat_results = []
        stat_results.append(numpy.amax(meas_results_calcs)) #max value
        stat_results.append(numpy.amin(meas_results_calcs)) #min value
        stat_results.append(numpy.median(meas_results_calcs)) #median 
        stat_results.append(numpy.mean(meas_results_calcs)) #mean 
        stat_results.append(numpy.std(meas_results_calcs)) #standard deviation 
        for entry in meas_results:
            temp_dict = collections.OrderedDict()
            temp_dict['start_time'] = entry[0]
            temp_dict['correction_frequency(Hz)'] = entry[1]
            temp_dict['max_value'] = entry[2]
            temp_dict['min_value'] = entry[3]
            temp_dict['offset(dBm)'] = entry[4]
            temp_dict['pass_fail_type'] = entry[5]
            temp_dict['test_plan'] = entry[6]
            temp_dict['pass_fail'] = entry[7]
            temp_dict['hardware_name'] = entry[8]
            temp_dict['data(dBm)'] = entry[9]
            temp_dict['instrument'] = entry[10]
            temp_dict['config_name'] = entry[11]
            temp_dict['active_testplan_name'] = entry[12]
        name_time = str(dt2ms(datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        print temp_i_list
        memcache.set(key, temp_dict)
        self.render('report_detail.html', stat_results = stat_results, meas_results = meas_results, 
                    profile = profile, download_key = newname)

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


class AnalysisExport(InstrumentDataHandler):
    def post(self):
        key = self.request.get('download_key')
        meas_results = memcache.get(key)
        headers = self.response.headers
        headers['Content-Type'] = 'text/csv'
        headers['Content-Disposition'] =  ('attachment; filename=export' + 
          str(datetime.now()) + '.csv')
        tmp = StringIO.StringIO()
        writer = csv.writer(tmp)
        counter = 0
        for item in meas_results:
            if counter == 0:
                writer.writerow(meas_results.keys())
                writer.writerow(meas_results.values())
            else:
                writer.writerow(meas_results.values()) 
            counter +=1
        contents = tmp.getvalue()
        tmp.close()
        self.response.out.write(contents)
