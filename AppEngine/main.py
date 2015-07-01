"""
This is the "data importer" module.  

It takes a http from input and stores it in the database.  It also allows you to display the results of the entry.
"""

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


authorized_users = ['charlie@gradientone.com',
                    'nedwards@gradientone.com',
                    'nickedwards@gmail.com'
#                    'nhannotte@gradientone.com',
#                    'wvennard@gradientone.com',
                    'test@example.com',
                   ]

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)
# Do we still need "autoescape = False"?

def author_creation():
    "Use the cookie to return the author"
    user = users.get_current_user()
    if user:
        active_user = user.email()
        active_user= active_user.split('@')
        author = active_user[0]
    return author

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_json(self, j):
    json_txt = json.dumps(j)
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.write(json_txt)

def root_mean_squared(test_data, test):
    "RMS measurement function that relies upon queries from test config and instrument data"
    print test
    RMS_time_start = float(test[0]["RMS_time_start"])
    RMS_time_stop = float(test[0]["RMS_time_stop"])  
    print 'rms stuff', RMS_time_start, RMS_time_stop
    sample_interval = 0.01
    row_RMS_time_start = RMS_time_start/sample_interval
    row_RMS_time_stop = RMS_time_stop/sample_interval
    sum = 0
    tempsq = 0
    i = 0
    for entry in test_data[int(row_RMS_time_start):(1+int(row_RMS_time_stop))]:
        tempsq = float(entry['CH1'])*float(entry['CH1'])
        sum += tempsq 
        i += 1
    z = sum/i
    rms = math.sqrt(z)
    return rms

def query_to_dict(result):
    query_dict = [r.to_dict() for r in result]
    return query_dict

def create_decimation(data):
    new_results = []
    print data
    for d in data:
        entries = d['cha'].split(',')
        for entry in entries:
            entry = entry.lstrip('[')
            entry = entry.rstrip(']')
            new_results.append(float(entry))
    new_results = new_results[:1000]
    results_arr = np.array(new_results)  #puts the test data in an array
    dec = decimate.decimate(results_arr, 10, ftype='fir', axis=0)  #performs the decimation function
    test_results = dec.tolist()
    return test_results

def getKey(row):
    return float(row.DTE)

class InstrumentDataHandler(webapp2.RequestHandler):


    authorized = False
    def write(self, *a, **kw): self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def authcheck(self, check_admin=False):
        user = users.get_current_user()
        if user:
            if user.email() in authorized_users:
                return True
            # todo: put in try block and handle exception
            cursor = db.GqlQuery("""SELECT * FROM UserDB 
                                  WHERE email = :1""", 
                                 user.email())
            result = cursor.get()
            if result:
                if user.email() == result.email:
                    if check_admin:
                        if result.admin:
                            authorized = True
                        else:
                            authorized = False
                    else:
                        authorized = True
            else:
                authorized = False
        else:
            authorized = False
        if not authorized:
            self.redirect('/static/autherror.html')
        return authorized

class DictModel(db.Model):


    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

def UserDB_key(name = 'default'):
    return db.Key.from_path('emails', name)


class UserDB(DictModel):


    email = db.StringProperty(required = True)
    company_nickname = db.StringProperty(required = True)
    admin = db.BooleanProperty(required = False)

def DemoDB_key(name = 'default'):
    return db.Key.from_path('messages', name)

class DemoDB(db.Model):


    receiver = db.StringProperty(required = True)
    sender = db.StringProperty(required = True)
    message = db.StringProperty(required = True)

def input_key(name = 'default'):
    return db.Key.from_path('inputs', name)


class Input(db.Model):


    frequency = db.FloatProperty(required = True)
    S11dB = db.FloatProperty(required = True)
    S12dB = db.FloatProperty(required = True)
    description = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

def TestDB_key(name = 'default'):
    return db.Key.from_path('tests', name)


class TestDB(DictModel):

    testplan_name = db.StringProperty(required = True)
    company_nickname = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    instrument_type = db.StringProperty(required = True)
    measurement_P2P = db.BooleanProperty(required = False)
    measurement_Peak = db.BooleanProperty(required = False)
    measurement_RMS = db.BooleanProperty(required = False)
    RMS_time_start = db.FloatProperty(required = False)
    RMS_time_stop = db.FloatProperty(required = False)
    measurement_RiseT = db.BooleanProperty(required = False)
    public = db.BooleanProperty(required = False)    
    commence_test = db.BooleanProperty(required = False)

def ConfigDB_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)


class ConfigDB(DictModel):

    company_nickname = db.StringProperty(required = True)
    hardware_name = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    instrument_name = db.StringProperty(required = False)
    source = db.StringProperty(required = False)
    horizontal_position = db.FloatProperty(required = False)
    horizontal_seconds_per_div = db.FloatProperty(required = False)
    vertical_position = db.FloatProperty(required = False)
    vertical_volts_per_division = db.FloatProperty(required = False)
    trigger_type = db.StringProperty(required = False)
    frequency_center = db.FloatProperty(required = False)
    frequency_span = db.FloatProperty(required = False)
    frequency_start = db.FloatProperty(required = False)
    frequency_stop = db.FloatProperty(required = False)
    power = db.FloatProperty(required = False)
    sample_rate = db.IntegerProperty(required = False)
    number_of_samples = db.IntegerProperty(required = False)
    start_measurement = db.BooleanProperty(required = False)

def OscopeDB_key(name = 'default'):
    return db.Key.from_path('oscope', name)


class OscopeDB(DictModel):


    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    data = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)
 
def BscopeDB_key(name = 'default'):
    return db.Key.from_path('bscope', name)


class BscopeDB(DictModel):

    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    cha = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)


def VNADB_key(name):
    return db.Key.from_path('vna', name)


class VNADB(DictModel):


    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    #slicename = db.StringProperty(required = True)
    FREQ = db.FloatProperty(required = True)
    created_date_time = db.DateTimeProperty(auto_now_add = True)
    #End_Date_Time = db.DateTimeProperty(required = False)
    S11dB = db.FloatProperty(required = True)
    S12dB = db.FloatProperty(required = True)
    S21dB = db.FloatProperty(required = True)
    S22dB = db.FloatProperty(required = True)
    S11ph = db.FloatProperty(required = True)
    S12ph = db.FloatProperty(required = True)
    S21ph = db.FloatProperty(required = True)
    S22ph = db.FloatProperty(required = True)
    header = db.StringProperty(required = True)
    options = db.StringProperty(required = True)


class MainPage(InstrumentDataHandler):


    def get(self):
        
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class ListUsersPage(InstrumentDataHandler):


    def get(self):
        users = db.GqlQuery("SELECT * FROM UserDB WHERE companyname = 'GradientOne'").fetch(None)
        print "ListUsersPage:get: users =",users
        if len(users) > 0:
            self.render('listusers.html',company=users[0].companyname,
                        users=users)
        else:
            self.render('listusers.html',company="new company?",
                        users=users)


class AdduserPage(InstrumentDataHandler):


    def get(self):
        u = users.get_current_user()
        if not u:
            self.redirect('/')
            return
        if not self.authcheck():
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + u.email())
            self.response.write(' you are not authorized to add users.')
            return
        admin_email = u.email()
        self.render('new_adduser.html')

    def post(self):
        username = self.request.get('email')
        companyname = self.request.get('companyname')  
        print "post: companyname =", companyname
        s = UserDB(parent = UserDB_key(), email = username, companyname = companyname)
        s.put()
        checked_box = self.request.get("admin")
        if checked_box:
            s.admin = True
            print s.admin
        else:
            s.admin = False
            print s.admin
        s.put()
        self.redirect('/input')


class OscopePage(InstrumentDataHandler):


    def get(self):
        #if not self.authcheck():
        f = open('tek0012ALL.csv')
        f = itertools.islice(f, 18, 100)
        reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
        out = [row for row in reader]
        render_json(self, out)

    def post(self, data):
        #if not self.authcheck():
        #    return
        print "you posted in the oscope handler"
        self.write.out(data)


class InstrumentsPage(InstrumentDataHandler):


    def get(self, author="", instrument_type="", instrument_name=""):
        #if not self.authcheck():
        #    return
        author = author_creation()
        instrument_name = instrument_name.split('.')
        if instrument_name[-1] == 'json':
            rows = db.GqlQuery("""SELECT * FROM ConfigDB WHERE author =:1 
                                and instrument_type =:2 
                                and instrument_name =:3""", 
                                author, instrument_type, instrument_name[0])
            inst_config = [r.to_dict() for r in rows]
            rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE 
                                name ='default-scope' ORDER BY TIME ASC""")
            default_data = [r.to_dict() for r in rows]
            inst_default = {"data":default_data, "inst_config":inst_config}
            render_json(self, inst_default)
        elif author and instrument_type and instrument_name:
            rows_inst_details = db.GqlQuery("""SELECT * FROM ConfigDB WHERE
                                             author =:1 and instrument_type 
                                             =:2 and instrument_name =:3""", 
                                             author, instrument_type, 
                                             instrument_name[0])
            self.render('instrument_detail.html')
        else:
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE author =:1", author)
            self.render('instruments.html', rows = rows)


class TestPlanSummary(InstrumentDataHandler):
    "present to the user a list of all configured test plans"
    
    def get(self, testplan_name=""):
        if testplan_name:
            key = testplan_name
            rows = memcache.get(key)
            if rows is None:
                rows = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            memcache.set(key, rows)
            test_config = [r.to_dict() for r in rows]
            memcache.set(key, rows)
            render_json(self, test_config)
        else:
            tests = db.GqlQuery("SELECT * FROM TestDB")
            self.render('testplansummary.html', tests = tests)


class TestResultsPage(InstrumentDataHandler):
    "present to the user all of the completed tests, with a path that supports specific test entries"

    def get(self, testplan_name="", name="", slicename=""):
        print testplan_name, name, slicename
        #if not self.authcheck():
        #    return
        author = author_creation()
        testplan_name_check = testplan_name.split('.')
        testplan_name = testplan_name_check[0]
        print testplan_name
        key = 'oscope' + testplan_name
        name = 'LED'
        slicename = str(1435107043000)
        data_key = 'oscopedata' + name + slicename
        if testplan_name_check[-1] == 'json':
            rows = memcache.get(data_key)
            if rows is None:
                logging.error("OscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                    AND slicename = :2 ORDER BY DTE ASC""", name, slicename)
                rows = list(rows)
                rows = sorted(rows, key=getKey)
            memcache.set(data_key, rows)
            test_data = [r.to_dict() for r in rows]  
            print test_data
            #start_of_test = test_data[0]['TIME']
            test = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            test = [t.to_dict() for t in test]
            print test
            #rms = {"rms":root_mean_squared(test_data, test)}
            test_result = {"data":test_data, "test_config":test} #"measurement":rms}
            render_json(self, test_result) 
        elif testplan_name:
            f = open(os.path.join('templates', 'testResultsPage.html'))
            self.response.write((f.read()))
        else:
            tests = db.GqlQuery("SELECT * FROM TestDB")
            rows = memcache.get(key)
            print "hi"
            if rows is None:
                logging.error("OscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                    AND slicename = :2 ORDER BY DTE ASC""", name, slicename)
                rows = list(rows)
                rows = sorted(rows, key=getKey)
            memcache.set(data_key, rows)
            self.render('index.html', tests = tests, rows = rows)

  
class CommunityTestsPage(InstrumentDataHandler):


    def get(self):
        rows = db.GqlQuery("SELECT * FROM TestDB WHERE public =:1", True)
        community_tests = [r.to_dict() for r in rows]
        render_json(self, community_tests)


class TestConfigInputPage(InstrumentDataHandler):

    def get(self):
        #if not self.authcheck():
        #    return
        self.render('testconfig.html')

    def is_checked(self,t,param):
        "Test checked and up date test object 't'."
        checked = self.request.get(param)
        if checked:
            setattr(t,param,True)
        else:
            setattr(t,param,False)

    def post(self):
        testplan_name = self.request.get('testplan_name')
        t = TestDB(parent = TestDB_key(testplan_name), 
            testplan_name = testplan_name, 
            company_nickname = self.request.get('company_nickname'), 
            author = self.request.get('author'),
            instrument_type = self.request.get('instrument_type'),
            RMS_time_start = float(self.request.get('RMS_time_start')),
            RMS_time_stop = float(self.request.get('RMS_time_stop')),)
        t.put()  # might help with making plan show up on list?
        key = testplan_name
        memcache.delete(key)
        checkbox_names = ["measurement_P2P", "measurement_Peak",
                          "measurement_RMS", "measurement_RiseT",
                           "public", "commence_test"]
        for name in checkbox_names:
            self.is_checked(t,name)
        t.put()
        self.redirect('/testplansummary')


class TestConfigOutputPage(InstrumentDataHandler):


    def get(self,testplan_name=""):
        print "testplan_name = ",testplan_name
        key = 'testplan_' + testplan_name 
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            memcache.set(key, configs)
        configs_out = [c.to_dict() for c in configs]
        render_json(self, configs_out)


class BscopeConfigInputPage(InstrumentDataHandler):

    def get(self):
        self.render('bscopeconfiginput.html')
    
    def is_checked(self,c,param):
        "Mesurement checked and up date test object 'c'."
        checked = self.request.get(param)
        if checked:
            setattr(c,param,True)
        else:
            setattr(c,param,False)
    
    def post(self):
        author = author_creation()
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        sample_rate = float(self.request.get('sample_rate'))
        number_of_samples = float(self.request.get('number_of_samples'))
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name,             
            sample_rate = sample_rate, number_of_samples = number_of_samples,
            )
        c.put() 
        checkbox_names = ["start_measurement"]
        for name in checkbox_names:
            self.is_checked(c,name)
        c.put()
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        memcache.delete(key)
        self.redirect('/configoutput/' + (author + '/' + instrument_type + '/' + instrument_name))

class ConfigInputPage(InstrumentDataHandler):


    def get(self):
        #if not self.authcheck():
         #   return
        self.render('configinput.html')

    def post(self):
        author = author_creation()
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        source = self.request.get('source')
        horizontal_position = float(self.request.get('horizontal_position'))
        horizontal_seconds_per_div = float(self.request.get('horizontal_seconds_per_div'))
        vertical_position = float(self.request.get('vertical_position'))
        vertical_volts_per_divsision = float(self.request.get('vertical_volts_per_divsision'))
        trigger_type = self.request.get('trigger_type')
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, 
            hardware_name = hardware_name, instrument_type = instrument_type, 
            instrument_name = instrument_name, source = source, 
            horizontal_position = horizontal_position, author = author,
            horizontal_seconds_per_div = horizontal_seconds_per_div, 
            vertical_position = vertical_position, 
            vertical_volts_per_division = vertical_volts_per_divsision, 
            trigger_type= trigger_type)
        c.put() 
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        memcache.delete(key)
        self.redirect('/configoutput/' + (author + '/' + instrument_type + '/' + instrument_name))


class VNAConfigInputPage(InstrumentDataHandler):


    def get(self):
        #if not self.authcheck():
        #    return
        self.render('vnaconfiginput.html')

    def post(self):
        author = author_creation()
        company_nickname = self.request.get('company_nickname')
        hardware_name = self.request.get('hardware_name')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        #frequency_center = float(self.request.get('frequency_center'))
        #frequency_span = float(self.request.get('frequency_span'))
        frequency_start = float(self.request.get('frequency_start'))
        frequency_stop = float(self.request.get('frequency_stop'))
        power = float(self.request.get('power'))
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name, 
            #frequency_center = frequency_center, frequency_span = frequency_span, 
            frequency_start = frequency_start, frequency_stop = frequency_stop,
            power = power)
        c.put() 
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        memcache.delete(key)
        redirect_url = author + '/' + instrument_type + '/' + instrument_name
        self.redirect('/configoutput/' + redirect_url)
        
   
class ConfigOutputPage(InstrumentDataHandler):


    def get(self, author="", instrument_type="", instrument_name=""):
        print "ConfigOutputPage"
        key = 'author & instrument_type & instrument_name = ', author + instrument_type + instrument_name
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = db.GqlQuery("SELECT * FROM ConfigDB WHERE instrument_name =:1", instrument_name)
            memcache.set(key, configs)
        configs_out = [c.to_dict() for c in configs]
        render_json(self, configs_out) 


class DataPage(InstrumentDataHandler):


    def get(self,name=""):
        #if not self.authcheck():
        #    return  # redirect to login later?
        query = """SELECT * FROM Input
                   WHERE description = '%s'
                   ORDER BY frequency ASC;""" % name
        print query
        datasets = db.GqlQuery(query)
        self.render('data.html', datasets = datasets)


class InputPage(InstrumentDataHandler):


    def get(self):
        #if not self.authcheck():
        #    return  # redirect to login later?
        self.render("front.html")
        print "you are in the get handler"

    def post(self):
        #if not self.authcheck():
        #    return  # redirect to login later?
        description = self.request.get("description")
        jsoninput = self.request.get("jsoninput")
        decoded = json.loads(jsoninput)
        new_decoded = {}
        for number_key, value_dict in decoded.iteritems():
            sub_dict = {}
            for value_key, value in value_dict.iteritems():
                sub_dict[value_key] = float(value)
            new_decoded[float(number_key)] = sub_dict
        for k in new_decoded:
            frequency = new_decoded[k]['FREQ']
            S11dB = new_decoded[k]['dB(S11)']
            S12dB = new_decoded[k]['dB(S12)']
            i = Input(parent = input_key(description), 
                frequency = frequency, S11dB = S11dB, 
                S12dB = S12dB, description = description)
            i.put()   
        self.redirect('/data/' + description)
        

class TestJSON(InstrumentDataHandler):


    def get(self):
        print "InstrumentDataHandler: get: you are in the get handler"

    def post(self):
        demo = json.loads(self.request.body)
        s = DemoDB(parent = DemoDB_key(), sender = demo['sender'], 
                   receiver = demo['receiver'], message = demo['message'])
        s.put()


class VNAData(InstrumentDataHandler):


    def get(self,name="", slicename=""):
        "retrieve Vector Network Analzyer data by insrument name"
        key = 'vna' + name + slicename
        rows = memcache.get(key)
        if rows is None:
            logging.error("VNA:get: query")
            rows = db.GqlQuery("""SELECT * FROM VNADB WHERE 
                                name =:1 AND slicename =:2 
                                ORDER BY TIME ASC""", 
                                name, slicename)
            rows = list(rows)
            rows = sorted(rows, key=getKey)
            memcache.set(key, rows)
        render_json(self, rows)

    def post(self, name=""):
        "store vector network analzyer data by name"
        start_time = time.time() 
        vna_content = json.loads(self.request.body)
        vna_data = vna_content['data']
        vna_options = vna_content['options']
        vna_header = vna_content['header']
        vna_config = vna_content['config']
        keys = list(vna_data.keys()) 
        to_save = []
        for k in keys[:50]:
                r = VNADB(parent = VNADB_key(name), name=name,
                    FREQ = float(vna_data[k]['FREQ']),
                    S11dB = float(vna_data[k]['dB(S11)']),
                    S12dB = float(vna_data[k]['dB(S12)']),
                    S21dB = float(vna_data[k]['dB(S21)']),
                    S22dB = float(vna_data[k]['dB(S22)']),
                    S11ph = float(vna_data[k]['PHS(S11)']),
                    S12ph = float(vna_data[k]['PHS(S12)']),
                    S21ph = float(vna_data[k]['PHS(S21)']),
                    S22ph = float(vna_data[k]['PHS(S22)']),
                    config = str(vna_config).strip('[]'),
                    header = str(vna_header).strip('[]'),
                    options = str(vna_options).strip('[]'),)
                to_save.append(r) 
        db.put(to_save)


class OscopeData(InstrumentDataHandler):


    def get(self,name="",slicename=""):
        "retrieve Oscilloscope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'oscopedata' + name + slicename
        rows = memcache.get(key)
        if rows is None:
            logging.error("OscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE name =:1
                                AND slicename = :2""", name, slicename)  
            rows = list(rows)
            print rows
            memcache.set(key, rows)
        data = query_to_dict(rows)
        output = {"data":data}
        render_json(self, output)


    def post(self,name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'oscopedata' + name + slicename
        oscope_content = json.loads(self.request.body)
        oscope_data = oscope_content['data']
        to_save = []
        for o in oscope_data:
            print o
            r = OscopeDB(parent = OscopeDB_key(name), name=name,
                         slicename=slicename,
                         config=str(oscope_content['config']),
                         data=(oscope_content['data']),
                         start_tse=(oscope_content['start_tse'])
                         )
        to_save.append(r) 
        memcache.set(key, to_save)
        db.put(to_save)

class BscopeData(InstrumentDataHandler):


    def get(self,name="",slicename=""):
        "retrieve BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'bscopedata' + name + slicename
        rows = memcache.get(key)
        if rows is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE name =:1
                                AND slicename = :2""", name, slicename)  
            rows = list(rows)
            memcache.set(key, rows)
        data = query_to_dict(rows)
        output = {"data":data}
        render_json(self, output)


    def post(self,name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'bscopedata' + name + slicename
        print 'bscope raw post handler'
        bscope_content = json.loads(self.request.body)
        to_save = []
        r = BscopeDB(parent = BscopeDB_key(name), name=name,
                         slicename=slicename,
                         config=str(bscope_content['config']),
                         cha=(bscope_content['data']),
                         start_tse=(bscope_content['start_tse'])
                         )
        to_save.append(r) 
        memcache.set(key, to_save)
        db.put(to_save)


class TestLibraryPage(InstrumentDataHandler):

    def get(self, instrument="", name="", start_tse=""):

        if instrument == "":
            rows = db.GqlQuery("SELECT * FROM BscopeDB")
            rows = list(rows)
            results_bscope = {}
            for r in rows:
                summary = set()
                summary.add((str(r.start_tse), str(r.name), str(r.config))) #make set to eliminate dupes
                summary = list(summary) #convert set to list
                summary = list(summary[0]) #breaks up list to individual items
                results_bscope[str(r.start_tse)] = summary
            rows = db.GqlQuery("SELECT * FROM OscopeDB")
            rows = list(rows)
            results_oscope = {}
            for r in rows:
                summary = set()
                summary.add((str(r.start_tse), str(r.name), str(r.config))) #make set to eliminate dupes
                summary = list(summary) #convert set to list
                summary = list(summary[0]) #breaks up list to individual items
                results_oscope[str(r.start_tse)] = summary
            self.render('testlibrary.html', results_bscope = results_bscope, results_oscope = results_oscope)

        elif instrument == 'bscopedata':
            raw = 'https://gradientone-test.appspot.com/bscopedata/' + name + '/' + start_tse
            dec = 'https://gradientone-test.appspot.com/dec/bscopedata/' + name + '/' + start_tse
            links = {"raw_data_url":raw, "dec_data_url":dec} 
            render_json(self, links) 

        elif instrument == 'oscopedata':
            print instrument, name, start_tse
            raw = 'https://gradientone-test.appspot.com/oscopedata/' + name + '/' + start_tse
            #dec = 'https://gradientone-test.appspot.com/dec/oscopedata/' + name + '/' + start_tse
            links = {"raw_data_url":raw} 
            render_json(self, links) 

        else:
            print instrument, name



class BscopeDataDec(InstrumentDataHandler):
   # work in progress

    def get(self,name="",start_tse=""):
        "retrieve decimated BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'bscopedatadec' + name + start_tse
        start_tse = int(start_tse)
        bscope_payload = memcache.get(key)
        if bscope_payload is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE name =:1
                                AND start_tse= :2 ORDER BY slicename ASC""", name, start_tse)  
            rows = list(rows)
            data = query_to_dict(rows)
            test_results = create_decimation(data)
            bscope_payload = {'config':data[0]['config'],'slicename':data[0]['slicename'],'cha':test_results, 'start_tse':data[0]['start_tse']}
            memcache.set(key, bscope_payload)
        render_json(self, bscope_payload)


    def post(self,name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'bscopedatadec' + name + slicename
        bscope_payload = self.request.body
        memcache.set(key, bscope_payload)



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/help', MainPage),
    ('/input', InputPage),
    ('/data/?', DataPage),
    ('/data/([a-zA-Z0-9-]+)', DataPage),
    ('/adduser', AdduserPage),
    ('/listusers', ListUsersPage),
    ('/instruments', InstrumentsPage),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', InstrumentsPage),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', InstrumentsPage),
    ('/configinput', ConfigInputPage),
    ('/vnaconfiginput', VNAConfigInputPage),
    ('/bscopeconfiginput', BscopeConfigInputPage),
    ('/configoutput/([a-zA-Z0-9-]+)', ConfigOutputPage),
    ('/configoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', ConfigOutputPage),
    ('/oscope.json', OscopePage),
    ('/testconfiginput', TestConfigInputPage),
    ('/testconfigoutput/([a-zA-Z0-9-]+)', TestConfigOutputPage),
    ('/testnuc', TestJSON),
    ('/testplansummary', TestPlanSummary),
    ('/testplansummary/([a-zA-Z0-9-]+)', TestPlanSummary),
    ('/communitytests', CommunityTestsPage),
    ('/testresults', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+)', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+.json)', TestResultsPage),
    ('/testlibrary', TestLibraryPage),
    ('/testlibrary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', TestLibraryPage),
    ('/testlibrary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', TestLibraryPage),
    ('/vnadata/([a-zA-Z0-9-]+)', VNAData),
    ('/oscopedata/([a-zA-Z0-9-]+)', OscopeData),
    ('/oscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', OscopeData),
    ('/bscopedata/([a-zA-Z0-9-]+)', BscopeData),
    ('/bscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', BscopeData),
    ('/dec/bscopedata/([a-zA-Z0-9-]+)', BscopeDataDec),
    ('/dec/bscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', BscopeDataDec),
], debug=True)



# danger!!  don't say it unless you mean it:  db.delete(VNADB.all(keys_only=True))  # deletes entire table!!
