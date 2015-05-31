"""
This is the "data importer" module.  

It takes a http from input and stores it in the database.  It also allows you to display the results of the entry.
"""
import os
import webapp2
import jinja2
import json
import logging
import datetime
import re
import csv
import itertools
import time
from time import gmtime, strftime
import collections
import hashlib
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import oauth
from google.appengine.api import memcache



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

def input_key(name = 'default'):
    return db.Key.from_path('inputs', name)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

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

#class OscopeData(db.Model):
#   """ Future DB code.

#    I will write code for the handling of the data from the tek OSCOPE for it go into the DB."""

#   time = db.FloatProperty(required = True)
#   ch1 = db.FloatProperty(required = True)
#   ch2 = db.FloatProperty(required = True)
#   ch3 = db.FloatProperty(required = True)
#   ch4 = db.FloatProperty(required = True)

#def Oscope_key(name = 'default'):
#   return db.Key.from_path('oscopedata', name)

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

class ConfigInputPage(InstrumentDataHandler):
    def get(self):
        #configiable = {"config:", "start"}
        #config_output = json.dumps([row for row in configiable])
        #self.response.write(config_output)
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

        c = ConfigDB(parent = ConfigDB_key(), company_nickname = company_nickname, 
            hardware_name = hardware_name, instrument_type = instrument_type, instrument_name = instrument_name, 
            source = source, horizontal_position = horizontal_position, 
            horizontal_seconds_per_div = horizontal_seconds_per_div, vertical_position = vertical_position, 
            vertical_volts_per_division = vertical_volts_per_divsision, trigger_type= trigger_type,)
        c.put() 
        memcache.delete('top')
        memcache.delete('timer')  
        
   
class ConfigOutputPage(InstrumentDataHandler):
    def get(self):
        key = 'top'
        key2 = 'timer'
        configs = memcache.get(key)
        if configs is None :
            logging.error("DB Query")
            configs = ConfigDB.all()
            query_time = time.time()
            configs = list(configs)
            memcache.set(key, configs)
            memcache.set(key2, query_time)
        delta = time.time() - memcache.get(key2)

        #config_query = db.GqlQuery("SELECT * FROM ConfigDB")
        #q = db.Query(ConfigDB)
        #configs = ConfigDB.all()
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps([c.to_dict() for c in configs]))
        print delta
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
    ('/configoutput.json', ConfigOutputPage),
    ('/oscope.json', OscopePage),
], debug=True)
