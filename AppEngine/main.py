"""
This is the "data importer" module.  

It takes a http from input and stores it in the database.  It also allows you to display the results of the entry.
"""
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

def render_json_cached(self,j):
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.write(j)

def root_mean_squared(test_data, test):
    "RMS measurement function that relies upon queries from test config and instrument data"
    RMS_time_start = float(test[0]["RMS_time_start"])
    RMS_time_stop = float(test[0]["RMS_time_stop"])  
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

def root_mean_squared_ta(test_data, RMS_time_start, RMS_time_stop, sample_interval):
    "RMS measurement function that relies upon queries from test config and instrument data"
    RMS_time_start = float(RMS_time_start)
    RMS_time_stop = float(RMS_time_stop) 
    sum = 0
    tempsq = 0
    i = 0
    for entry in test_data[int(RMS_time_start/sample_interval):(1+int(RMS_time_stop/sample_interval))]:
        tempsq = entry*entry
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

def convert_str_to_cha_list(string):
    sample_data = string[0]['cha']
    bracket_free_data = sample_data[1:-1]
    cha_list = bracket_free_data.split(',')
    cha_list =  [float(x) for x in cha_list]
    return cha_list

def dropdown_creation():
    key = 'instrumentsDB' 
    dropdown = memcache.get(key)
    if dropdown == None:
        logging.error("BscopeData:get: query")
        b = db.GqlQuery("""SELECT * FROM BscopeDB LIMIT 1""")
        o = db.GqlQuery("""SELECT * FROM OscopeDB LIMIT 1""")
        rows_b = list(b)
        rows_o = list(o)
        results_b = query_to_dict(rows_b)
        results_o = query_to_dict(rows_o)
        dropdown = []
        if results_b != []: 
            dropdown.append('BitScope')
        if results_o != []:
            dropdown.append('Tektronix')
        memcache.set(key, dropdown)
    return dropdown

def create_psettings(data):
    data = str(data[0]['config'])
    data = data.split(',')
    temp_list = []
    for d in data[:5]:
        temp_list.append(d)
    temp_dict = {}
    for item in temp_list[1:-1]:
        item = item.split(':')
        temp_dict[item[0].strip().strip('u').strip('\'')] = int((item[1].strip().strip('L')))
    t = temp_list[0]
    t = t.split(':')
    del t[0]
    temp_dict[t[0].strip().strip('{').strip('u').strip('\'')] = int((t[1].strip()))
    t = temp_list[-1]
    t = t.split(':')
    temp_dict[t[0].strip().strip('u').strip('\'')] = int((t[1].strip().strip('}')))
    return temp_dict
    
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


class FileBlob(db.Model):
    blob_key = blobstore.BlobReferenceProperty(required=True)


class UploadURLGenerator(InstrumentDataHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload/upload_file')
        self.response.out.write(upload_url)
    def post(self):
        UploadURLGenerator.get(self)


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0] 
            dbfile = FileBlob(blob_key=upload.key())
            dbfile.put()
            self.redirect('/upload/success')
        except:
            self.redirect('/upload_failure.html')


class FileUploadSuccess(InstrumentDataHandler):
    def get(self):
        self.response.out.write("File Upload Successful")


class FileUploadFailure(InstrumentDataHandler):
    def get(self):
        self.response.out.write("File Upload Failed")


def TestDB_key(name = 'default'):
    return db.Key.from_path('tests', name)

class TestDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    author = db.StringProperty(required = False)
    date_created = db.DateTimeProperty(auto_now_add = False)
    instrument_type = db.StringProperty(required = False)
    measurement_P2P = db.BooleanProperty(required = False)
    measurement_Peak = db.BooleanProperty(required = False)
    measurement_RMS = db.BooleanProperty(required = False)
    RMS_time_start = db.FloatProperty(required = False)
    RMS_time_stop = db.FloatProperty(required = False)
    measurement_RiseT = db.BooleanProperty(required = False)
    public = db.BooleanProperty(required = False)    
    commence_test = db.BooleanProperty(required = False)


def TestResultsDB_key(name = 'default'):
    return db.Key.from_path('testresults', name)

class TestResultsDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    plot_settings = db.StringProperty(required = False)
    dec_data_url = db.StringProperty(required = False)
    raw_data_url = db.StringProperty(required = False)
    start_tse = db.IntegerProperty(required = False)
    test_complete = db.IntegerProperty(required = False)

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
    test_plan = db.BooleanProperty(required = True)
    testplan_name = db.StringProperty(required = False)



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
    i_settings = db.StringProperty(required = True)
    p_settings = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    cha = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)


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
    def get(self, hardwarename="", testplan_name=""):
        if hardwarename and testplan_name:
            rows = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            test_config = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE testplan_name =:1", testplan_name)
            inst_config = query_to_dict(rows)
            config = {'test_config':test_config, 'inst_config':inst_config}
            render_json(self, config)
        else:
            rows = db.GqlQuery("SELECT * FROM TestDB WHERE commence_test =:1", True)
            rows = list(rows)            
            test_config = query_to_dict(rows)
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE test_plan =:1", True)
            rows = list(rows)
            inst_config = query_to_dict(rows)
            for t in test_config:
                #print t['testplan_name']
                for i in inst_config: 
                    #print i['testplan_name']
                    if i['testplan_name'] == t['testplan_name']:
                        t['inst_config'] = i
            render_json(self, test_config)



class TestResultsPage(InstrumentDataHandler):
    "present to the user all of the completed tests, with a path that supports specific test entries"
    def get(self, testplan_name="", name="", slicename=""):
        #if not self.authcheck():
        #    return
        author = author_creation()
        testplan_name_check = testplan_name.split('.')
        testplan_name = testplan_name_check[0]
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
            #start_of_test = test_data[0]['TIME']
            test = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            test = [t.to_dict() for t in test]
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
        company_nickname = self.request.get('company_nickname')
        author = self.request.get('author')
        instrument_type = self.request.get('instrument_type')
        instrument_name = self.request.get('instrument_name')
        hardware_name = self.request.get('hardware_name')
        RMS_time_start = float(self.request.get('RMS_time_start'))
        RMS_time_stop = float(self.request.get('RMS_time_stop'))
        sample_rate = int(self.request.get('sample_rate'))
        number_of_samples = int(self.request.get('number_of_samples'))
        t = TestDB(parent = TestDB_key(testplan_name), 
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            instrument_type = instrument_type,
            RMS_time_start = RMS_time_start,
            RMS_time_stop = RMS_time_stop,)
        t.put()  # might help with making plan show up on list?
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name,             
            sample_rate = sample_rate, number_of_samples = number_of_samples,
            test_plan = True,
            testplan_name = testplan_name,
            )
        c.put() 
        key = testplan_name
        memcache.delete(key)
        checkbox_names = ["measurement_P2P", "measurement_Peak",
                          "measurement_RMS", "measurement_RiseT",
                           "public", "commence_test"]
        for name in checkbox_names:
            self.is_checked(t,name)
        t.put()
        self.redirect('/testplansummary/' + hardware_name)


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
        sample_rate = int(self.request.get('sample_rate'))
        number_of_samples = int(self.request.get('number_of_samples'))
        c = ConfigDB(parent = ConfigDB_key(instrument_name), 
            company_nickname = company_nickname, author = author,
            hardware_name = hardware_name, instrument_type = instrument_type,
            instrument_name = instrument_name,             
            sample_rate = sample_rate, number_of_samples = number_of_samples,
            test_plan = False,
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
            r = OscopeDB(parent = OscopeDB_key(name), name=name,
                         slicename=slicename,
                         config=str(oscope_content['config']),
                         data=(oscope_content['data']),
                         start_tse=(oscope_content['start_tse'])
                         )
        to_save.append(r) 
        memcache.set(key, to_save)
        db.put(to_save)


class TestResultsData(InstrumentDataHandler):

    def get(self,testplan_name="",start_tse=""):
        "retrieve BitScope data by intstrument name and time slice name"
        #if not self.authcheck():
        #    return
        key = 'testresults' + testplan_name + start_tse
        rows = memcache.get(key)
        if rows is None:
            logging.error("BscopeData:get: query")
            rows = db.GqlQuery("""SELECT * FROM TestResultsDB WHERE testplan_name =:1
                            AND start_tse = :2""", testplan_name, start_tse)  
            rows = list(rows)
            memcache.set(key, rows)
        data = query_to_dict(rows)
        output = {"data":data}
        render_json(self, output)

    def post(self,testplan_name="",start_tse=""):
        "store data by intstrument name and time slice name"
        key = 'testresults' + testplan_name + start_tse
        print 'test plan raw post handler'
        testresults_content = json.loads(self.request.body)
        to_save = []
        r = TestResultsDB(parent = TestResultsDB_key(testplan_name), testplan_name=testplan_name,
                    plot_settings=str(testresults_content['p_settings']),
                    dec_data_url=str(testresults_content['dec_data_url']),
                    raw_data_url=str(testresults_content['raw_data_url']),
                    start_tse=(testresults_content['start_tse'])
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
        cha_list = convert_str_to_cha_list(data)
        data[0]['cha'] = cha_list
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
                         p_settings=str(bscope_content['p_settings']),
                         i_settings=str(bscope_content['i_settings']),
                         cha=(bscope_content['cha']),
                         start_tse=(bscope_content['start_tse'])
                         )
        to_save.append(r) 
        memcache.set(key, to_save)
        db.put(to_save)


class SearchPage(InstrumentDataHandler):
    def get(self, name="", slicename="", start_tse=""):
        dropdown = dropdown_creation()
        self.render('search.html', dropdown = dropdown)
    def post(self):
        dropdown = dropdown_creation()
        name = self.request.get('name')
        start_tse = int(self.request.get('start_tse'))
        slicename = self.request.get('slicename')
        instrument = self.request.get('instrument')
        config = self.request.get('config')
        if instrument == 'BitScope':
            instrument = BscopeDB.gql
        elif instrument == 'Tektronix':
            instrument = OscopeDB.gql
        #query = instrument("where name = :1 and start_tse =:2 and slicename =:3 and config =:4", name, start_tse, slicename, config)

        results = set()
               #summary.add((str(r.start_tse), str(r.name), str(r.config))) #make set to eliminate dupes
        query=BscopeDB.all()
        start_tse_query = query.filter("start_tse =",start_tse).run()
        for i in start_tse_query:
            results.add((str(i.start_tse), str(i.name)))
        config_query = query.filter("config =",config).run()
        for i in config_query:
            results.add((str(i.start_tse), str(i.name)))
        results = list(results)
        print results
        self.render('search.html', results = results, dropdown = dropdown, name = name, slicename = slicename, start_tse = start_tse, config = config )


class TestAnalyzerPage(InstrumentDataHandler):
    #work in progress.  To do:  modularize parsing and measurment calls.
    def get(self, instrument="", name="", start_tse=""):
        if instrument == 'bscopedata':
            key = 'bscopedata' + name + start_tse
            start_tse = int(start_tse)
            rows = memcache.get(key)
            if rows is None:
                logging.error("BscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE name =:1
                                AND start_tse=:2 ORDER BY slicename ASC """, name, start_tse)  
                rows = list(rows)
                memcache.set(key, rows)
            data = query_to_dict(rows)
            config_settings = create_psettings(data)
            start_time = 0 #miliseconds
            stop_time = config_settings['Total_Slices'] * config_settings['Slice_Size(msec)'] * config_settings['Raw_msec_btw_samples']#miliseconds
            si = config_settings['Raw_msec_btw_samples']
            self.render('testanalyzer.html', test_sample = start_tse, start_time = start_time, stop_time = stop_time)        
    def post(self, instrument="", name="", start_tse=""):
        if instrument == 'bscopedata':
            key = 'bscopedata' + name + start_tse
            start_tse = int(start_tse)
            rows = memcache.get(key)
            if rows is None:
                logging.error("BscopeData:get: query")
                rows = db.GqlQuery("""SELECT * FROM BscopeDB WHERE name =:1
                                AND start_tse=:2 ORDER BY slicename ASC """, name, start_tse)  
                rows = list(rows)
                memcache.set(key, rows)
            data = query_to_dict(rows)
            config_settings = create_psettings(data)
            start_time = 0 #miliseconds
            stop_time = config_settings['Total_Slices'] * config_settings['Slice_Size(msec)'] * config_settings['Raw_msec_btw_samples']#miliseconds
            si = config_settings['Raw_msec_btw_samples']
            temp = []
            for item in data:
                z = ast.literal_eval(item['cha'])
                temp.extend(z)
            RMS_time_start = self.request.get('RMS_time_start')
            RMS_time_stop = self.request.get('RMS_time_stop')
            rms = root_mean_squared_ta(temp, RMS_time_start, RMS_time_stop, si)
            self.render('testanalyzer.html', test_sample = start_tse, start_time = start_time, stop_time = stop_time, rms = rms)


class TestLibraryPage(InstrumentDataHandler):
    def get(self, instrument="", name="", start_tse=""):
        start_tse_check = start_tse.split('.')
        start_tse = start_tse_check[0]
        if instrument == 'bscopedata' and start_tse_check[-1] == 'json':
            key = 'psettings' + name + start_tse
            psettings = memcache.get(key)
            if psettings == None:
                logging.error("BscopeData:get: query")
                query = db.GqlQuery("""SELECT * FROM BscopeDB WHERE start_tse = :1 LIMIT 1""", int(start_tse))
                rows = list(query)
                data = query_to_dict(rows)
                psettings = data[0]['p_settings']
                memcache.set(key, psettings)
            raw = 'https://gradientone-test.appspot.com/bscopedata/' + name + '/' + start_tse
            dec = 'https://gradientone-test.appspot.com/dec/bscopedata/' + name + '/' + start_tse
            links = {"raw_data_url":raw, "dec_data_url":dec, 'p_settings':psettings}
            render_json(self, links) 
        elif instrument == 'oscopedata' and start_tse_check[-1] == 'json':
            print instrument, name, start_tse
            raw = 'https://gradientone-test.appspot.com/oscopedata/' + name + '/' + start_tse
            #dec = 'https://gradientone-test.appspot.com/dec/oscopedata/' + name + '/' + start_tse
            links = {"raw_data_url":raw} 
            render_json(self, links) 
        elif instrument == 'bscopedata':
            f = open(os.path.join('templates', 'testLibResults.html'))
            self.response.write((f.read()))
        elif instrument == 'oscopedata':
            f = open(os.path.join('templates', 'testLibResults.html'))
            self.response.write((f.read()))
        else:
            query = db.Query(BscopeDB, projection=['start_tse', 'name'], distinct=True).order('-start_tse').fetch(limit = 10)
            rows = list(query)
            results_bscope = rows
            query = db.Query(OscopeDB, projection=['start_tse', 'name'], distinct=True).order('-start_tse').fetch(limit = 10)
            rows = list(query)
            results_oscope = rows
            library = results_bscope, results_oscope
            results_bscope = library[0]
            results_oscope = library[1]
            self.render('testlibrary.html', results_bscope = results_bscope, results_oscope = results_oscope)


class TestCompletePage(InstrumentDataHandler):
    def post(self, testplan_name="", stop_tse=""):
        test_complete_content = json.loads(self.request.body)
        testplan_name = test_complete_content['testplan_name']
        stop_tse = test_complete_content['stop_tse']
        result = db.GqlQuery("SELECT * FROM TestResultsDB WHERE testplan_name =:1", testplan_name)
        for r in result:
            r.stop_tse = stop_tse
            r.put()   
        result = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
        for r in result:
            r.commence_test = False
            r.put()


class NewTestLibraryPage(InstrumentDataHandler):
    def get(self):
        rows = db.GqlQuery("SELECT * FROM TestResultsDB")
        rows = list(rows)            
        test_results = query_to_dict(rows)
        render_json(self, test_results)


class BscopeDataDec(InstrumentDataHandler):
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
            bscope_payload = {'i_settings':data[0]['i_settings'], 'p_settings':data[0]['p_settings'] ,'slicename':data[0]['slicename'],'cha':test_results, 'start_tse':data[0]['start_tse']}
            memcache.set(key, bscope_payload)
            render_json(self, bscope_payload)
        else:
            if type(bscope_payload) == str:
                render_json_cached(self, bscope_payload)
            else:
                #bscope_payload = dict(bscope_payload)
                render_json(self, bscope_payload)
    def post(self,name="",slicename=""):
        "store data by intstrument name and time slice name"
        key = 'bscopedatadec' + name + slicename
        bscope_payload = self.request.body
        memcache.set(key, bscope_payload)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/help', MainPage),
    ('/adduser', AdduserPage),
    ('/listusers', ListUsersPage),
    ('/instruments', InstrumentsPage),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', InstrumentsPage),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', InstrumentsPage),
    ('/configinput', ConfigInputPage),
    ('/bscopeconfiginput', BscopeConfigInputPage),
    ('/configoutput/([a-zA-Z0-9-]+)', ConfigOutputPage),
    ('/configoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', ConfigOutputPage),
    ('/testconfiginput', TestConfigInputPage),
    ('/testconfigoutput/([a-zA-Z0-9-]+)', TestConfigOutputPage),
    ('/testplansummary/([a-zA-Z0-9-]+)', TestPlanSummary),
    ('/testplansummary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', TestPlanSummary),
    ('/communitytests', CommunityTestsPage),
    ('/search', SearchPage),
    ('/testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', TestCompletePage),
    ('/testresults', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+)', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+.json)', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', TestResultsData),
    ('/testlibrary', TestLibraryPage),
    ('/testlibrary.json', NewTestLibraryPage),
    ('/testlibrary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', TestLibraryPage),
    ('/testlibrary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', TestLibraryPage),
    ('/testanalyzer/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', TestAnalyzerPage),
    ('/oscopedata/([a-zA-Z0-9-]+)', OscopeData),
    ('/oscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', OscopeData),
    ('/bscopedata/([a-zA-Z0-9-]+)', BscopeData),
    ('/bscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', BscopeData),
    ('/bscopedata/dec/([a-zA-Z0-9-]+)', BscopeDataDec),
    ('/bscopedata/dec/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', BscopeDataDec),
    ('/upload/geturl', UploadURLGenerator),
    ('/upload/upload_file', FileUploadHandler),
    ('/upload/success',FileUploadSuccess),
    ('/upload/failure',FileUploadFailure),
], debug=True)



# danger!!  don't say it unless you mean it:  db.delete(VNADB.all(keys_only=True))  # deletes entire table!!
