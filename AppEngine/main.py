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

authorized_users = ['charlie@gradientone.com',
                    'nedwards@gradientone.com',
#                    'nhannotte@gradientone.com',
#                    'wvennard@gradientone.com',
                    'test@example.com',
                   ]

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)
# Do we still need "autoescape = False"?

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

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
            cursor = db.GqlQuery("SELECT * FROM UserDB WHERE email = :1", 
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

def UserDB_key(name = 'default'):
    return db.Key.from_path('emails', name)

class UserDB(db.Model):
    email = db.StringProperty(required = True)
    companyname = db.StringProperty(required = True)
    admin = db.BooleanProperty(required = False)

def DemoDB_key(name = 'default'):
    return db.Key.from_path('messages', name)

class DemoDB(db.Model):
    receiver = db.StringProperty(required = True)
    sender = db.StringProperty(required = True)
    message = db.StringProperty(required = True)

def input_key(name = 'default'):
    return db.Key.from_path('inputs', name)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class TestDB(DictModel):
    testplan_name = db.StringProperty(required = True)
    company_nickname = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    measurement_P2P = db.BooleanProperty(required = False)
    measurement_Peak = db.BooleanProperty(required = False)
    measurement_RMS = db.BooleanProperty(required = False)
    RMS_time_start = db.FloatProperty(required = False)
    RMS_time_stop = db.FloatProperty(required = False)
    measurement_RiseT = db.BooleanProperty(required = False)
    public = db.BooleanProperty(required = False)    
    commence_test = db.BooleanProperty(required = False)

def TestDB_key(name = 'default'):
    return db.Key.from_path('tests', name)

class ConfigDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    hardware_name = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    instrument_name = db.StringProperty(required = False)
    source = db.StringProperty(required = False)
    horizontal_position = db.FloatProperty(required = False)
    horizontal_seconds_per_div = db.FloatProperty(required = False)
    vertical_position = db.FloatProperty(required = False)
    vertical_volts_per_division = db.FloatProperty(required = False)
    trigger_type = db.StringProperty(required = False)
    #trigger_value = db.FloatProperty(required = False)

def ConfigDB_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)

def OscopeDB_key(name):
    return db.Key.from_path('oscope', name)

class OscopeDB(DictModel):
    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    TIME = db.DateTimeProperty(required = True)
    CH1 = db.FloatProperty(required = True)
    CH2 = db.FloatProperty(required = True)
    CH3 = db.FloatProperty(required = True)
    CH4 = db.FloatProperty(required = True)

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
        self.render('adduser.html')

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


class Input(db.Model):
    frequency = db.FloatProperty(required = True)
    S11dB = db.FloatProperty(required = True)
    S12dB = db.FloatProperty(required = True)
    description = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def render(self):
        self._render_text = self.inputdata.replace('\n', '<br>')
        return render_str("post.html", p = self)


class OscopePage(InstrumentDataHandler):
    def get(self):
        #if not self.authcheck():
        f = open('tek0012ALL.csv')
        f = itertools.islice(f, 18, 100)
        reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
        out = json.dumps([row for row in reader])
        self.response.headers['Content-Type'] = 'application/js; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(out)
        #self.response.write("(" + out + ")")
        #for row in reader:
            #r = OscopeData(parent = Oscope_key(), time = TIME, ch1 = CH1, ch2 = CH2, ch3 = CH3, ch4 = CH4)
            #r.put()

    def post(self, data):
        #if not self.authcheck():
        #    return
        print "you posted in the oscope handler"
        self.write.out(data)

class InstrumentsPage(InstrumentDataHandler):
    def get(self):
        if not self.authcheck():
            return
        self.render('instruments.html')

class TestResultsPage(InstrumentDataHandler):
    "present to the user all of the completed tests, with a path that supports specific test entries"
    def get(self, testplan_name=""):
        if testplan_name:
            print "test results here"
            key = 'oscope' + testplan_name
            rows = memcache.get(key)
            if rows is None:
                rows = db.GqlQuery("SELECT * FROM OscopeDB ORDER BY TIME ASC")
            memcache.set(key, rows)

            print rows
            #self.response.write(json.dumps([r.to_dict() for r in rows]))
            print  "Test ResultsPage: get: rows = ", [r.to_dict() for r in rows]
            #decoded = json.loads(entries)
            #decoded_sorted = sorted(decoded, key=lambda item: item['TIME'])
            #self.response.write(decoded_sorted)

            test = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            test = json.dumps([t.to_dict() for t in test])
            test = json.loads(test)
            print test
            #start_of_test = decoded_sorted[0]['TIME']
            RMS_time_start = float(test[0]["RMS_time_start"])
            RMS_time_stop = float(test[0]["RMS_time_stop"])
            print RMS_time_start
            print RMS_time_stop
            sum = 0
            tempsq = 0
            i = 0
            #for entry in decoded_sorted[0:10]:
            #    tempsq = float(entry['CH1'])*float(entry['CH1'])
            #    sum += tempsq
            #    i += 1
           # z = sum/i
            #rms = math.sqrt(z)
            #print rms

            
        else:
            tests = db.GqlQuery("SELECT * FROM TestDB")
            self.render('testresults.html', tests = tests)




class TestConfigInputPage(InstrumentDataHandler):
    def get(self):
        self.render('testconfig.html')

    def post(self):
        testplan_name = self.request.get('testplan_name')
        company_nickname = self.request.get('company_nickname')
        author = self.request.get('author')
        instrument_type = self.request.get('instrument_type')
        measurement_P2P = self.request.get('measurement_P2P')
        measurement_Peak = self.request.get('measurement_Peak')
        mesaurement_RMS = self.request.get('measurement_RMS')
        RMS_time_start = float(self.request.get('RMS_time_start'))
        RMS_time_stop = float(self.request.get('RMS_time_stop'))
        measurement_RiseT = self.request.get('measurement_RiseT')
        public = self.request.get('public')
        commence_test = self.request.get('commence_test')
        print commence_test
        print RMS_time_start
        print RMS_time_stop

        t = TestDB(parent = TestDB_key(testplan_name), testplan_name = testplan_name, company_nickname = company_nickname, author = author, instrument_type = instrument_type, 
            RMS_time_start = RMS_time_start, 
            RMS_time_stop = RMS_time_stop,)
        t.put()
        key = testplan_name
        memcache.delete(key)

        checked_box = self.request.get("measurement_P2P")
        if checked_box:
            t.measurement_P2P = True
        else:
            t.measurement_P2P = False
        t.put()

        checked_box = self.request.get("measurement_Peak")
        if checked_box:
            t.measurement_Peak = True
        else:
            t.measurement_Peak = False
        t.put()

        checked_box = self.request.get("measurement_RMS")
        if checked_box:
            t.measurement_RMS = True
        else:
            t.measurement_RMS = False
        t.put()

        checked_box = self.request.get("measurement_RiseT")
        if checked_box:
            t.measurement_RiseT = True
        else:
            t.measurement_RiseT = False
        t.put()

        checked_box = self.request.get("public")
        if checked_box:
            t.public = True
        else:
            t.public = False
        t.put()

        checked_box = self.request.get("commence_test")
        if checked_box:
            t.commence_test = True
        else:
            t.commence_test = False
        t.put()

        self.redirect('/testresults')
        #self.redirect('/testconfigoutput/'+testplan_name)

class TestConfigOutputPage(InstrumentDataHandler):
    def get(self,testplan_name=""):
        print "testplan_name = ",testplan_name
        key = 'testplan_' + testplan_name 
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = db.GqlQuery("SELECT * FROM TestDB WHERE testplan_name =:1", testplan_name)
            memcache.set(key, configs)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps([c.to_dict() for c in configs]))


class ConfigInputPage(InstrumentDataHandler):
    def get(self):
        self.render('configinput.html')

    def post(self):
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

        c = ConfigDB(parent = ConfigDB_key(instrument_name), company_nickname = company_nickname, 
            hardware_name = hardware_name, instrument_type = instrument_type, instrument_name = instrument_name, 
            source = source, horizontal_position = horizontal_position, 
            horizontal_seconds_per_div = horizontal_seconds_per_div, vertical_position = vertical_position, 
            vertical_volts_per_division = vertical_volts_per_divsision, trigger_type= trigger_type,)
        c.put() 
        key = 'instrument_name = ', instrument_name
        print key
        memcache.delete(key)
        self.redirect('/configoutput/'+instrument_name)
        
   
class ConfigOutputPage(InstrumentDataHandler):
    def get(self,instrument_name=""):
        key = 'instrument_name = ', instrument_name
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = db.GqlQuery("SELECT * FROM ConfigDB WHERE instrument_name =:1", instrument_name)
            memcache.set(key, configs)
        #config_query = db.GqlQuery("SELECT * FROM ConfigDB")
        #q = db.Query(ConfigDB)
        #configs = ConfigDB.all()
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps([c.to_dict() for c in configs]))

        #dict_of_vars = dict((str(config.company_nickname), {'company_nickname': config.company_nickname, 'source': config.source, 'hardware_name': config.hardware_name, 'instrument_type': config.instrument_type, 'instrument_name': config.instrument_name, 'horizontal_position': config.horizontal_position, 'horizontal_seconds_per_div': config.horizontal_seconds_per_div, 'vertical_position': config.vertical_position, 'vertical_volts_per_division': config.vertical_volts_per_division, 'trigger_type': config.trigger_type}) for config in configs)
        
        #out = json.dumps(dict_of_vars)
        #self.response.write(out)
#dict_of_entities = dict((str(entity.key()), {'name': entity.name, 'size': entity.size}) for entity in entities)

        

class DataPage(InstrumentDataHandler):
    def get(self,name=""):
        if not self.authcheck():
            return  # redirect to login later?
        query = """SELECT * FROM Input
                   WHERE description = '%s'
                   ORDER BY frequency ASC;""" % name
        print query
        datasets = db.GqlQuery(query)
        self.render('data.html', datasets = datasets)

class InputPage(InstrumentDataHandler):
    def get(self):
        if not self.authcheck():
            return  # redirect to login later?
        self.render("front.html")
        print "you are in the get handler"

    def post(self):

        if not self.authcheck():
            return  # redirect to login later?
        print "you are in the InputPage posthandler"
        description = self.request.get("description")
        print "InputPage: post: description =", description
        jsoninput = self.request.get("jsoninput")
        #print jsoninput
        decoded = json.loads(jsoninput)
        print "InputPage:post decoded =",decoded
        new_decoded = {}
        for number_key, value_dict in decoded.iteritems():
            print "InputPage:post decoded =",number_key,value_dict
            sub_dict = {}
            for value_key, value in value_dict.iteritems():
                sub_dict[value_key] = float(value)
            new_decoded[float(number_key)] = sub_dict

        for k in new_decoded:
            frequency = new_decoded[k]['FREQ']
            S11dB = new_decoded[k]['dB(S11)']
            S12dB = new_decoded[k]['dB(S12)']
            i = Input(parent = input_key(description), frequency = frequency, S11dB = S11dB, S12dB = S12dB, description = description)
            i.put()
        
        self.redirect('/data/' + description)
        
class TestJSON(InstrumentDataHandler):
    def get(self):
        print "InstrumentDataHandler: get: you are in the get handler"

    def post(self):
        print "InstrumentDataHandler:post"
        demo = json.loads(self.request.body)
        print "InstrumentDataHandler:post demo =",demo
        print "demo =",demo
        s = DemoDB(parent = DemoDB_key(), sender = demo['sender'], 
                   receiver = demo['receiver'], message = demo['message'])
        s.put()

class OscopeData(InstrumentDataHandler):
    def get(self,name="",slicename=""):
        "retrieve data by intstrument name and time slice name"
        print "OscopeData: get: name =",name
        print "OscopeData: get: slicename =",slicename
        key = 'oscope' + name + slicename
        rows = memcache.get(key)
        if rows is None:
            logging.error("OscopeData:get: query")
            query = """SELECT * FROM OscopeDB
                         WHERE name = '%(name)s'
                         AND slicename = '%(slicename)s'
                         ORDER BY TIME ASC;
                    """  % {'name':name,'slicename':slicename}
            logging.error("OscopeData:get: query")
            rows = db.GqlQuery(query)
            memcache.set(key, rows)

        #config_query = db.GqlQuery("SELECT * FROM ConfigDB")
        #q = db.Query(ConfigDB)
        #configs = ConfigDB.all()
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps([r.to_dict() for r in rows]))

    def post(self,name=""):
        "store data by intstrument name and time slice name"
        #print "OscopeData: post: name =",name
        oscope_data = json.loads(self.request.body)
        #print "oscope_data['slicename']=",oscope_data['slicename']
        #print "oscope_data['config']=",oscope_data['config']
        def getKey(row):
            return float(row['TIME'])
        sorted_data = sorted(oscope_data['data'], key=getKey)
        #print "post:sorted_data =",sorted_data
        t = time.time()
        for row in sorted_data:
            dt = datetime.datetime.fromtimestamp(t + float(row['TIME']))
            r = OscopeDB(parent = OscopeDB_key(name), name=name,
                         slicename=oscope_data['slicename'],
                         config=str(oscope_data['config']),
                         TIME=dt,
                         CH1=float(row['CH1']),
                         CH2=float(row['CH2']),
                         CH3=float(row['CH3']),
                         CH4=float(row['CH4']))
            r.put()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/help', MainPage),
    ('/input', InputPage),
    ('/data/?', DataPage),
    ('/data/([a-zA-Z0-9-]+)', DataPage),
    ('/adduser', AdduserPage),
    ('/listusers', ListUsersPage),
    ('/instruments', InstrumentsPage),
    ('/configinput', ConfigInputPage),
    ('/configoutput/([a-zA-Z0-9-]+)', ConfigOutputPage),
    ('/oscope.json', OscopePage),
    ('/testconfiginput', TestConfigInputPage),
    ('/testconfigoutput/([a-zA-Z0-9-]+)', TestConfigOutputPage),
    ('/testnuc', TestJSON),
    ('/testresults', TestResultsPage),
    ('/testresults/([a-zA-Z0-9-]+)', TestResultsPage),
    ('/oscopedata/([a-zA-Z0-9-]+)', OscopeData),
    ('/oscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', OscopeData),
], debug=True)
