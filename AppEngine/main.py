"""
This is the "data importer" module.  

It takes a http from input and stores it in the database.  It also allows you to display the results of the entry.
"""
import os
import webapp2
import jinja2
import json
import datetime
import re
from time import gmtime, strftime
import collections
import hashlib
from google.appengine.ext import db
from google.appengine.api import users

authorized_users = ['charlie@gradientone.com',
                    'nedwards@gradientone.com',
                    'nhannotte@gradientone.com',
                    'wvennard@gradientone.com',
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
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def authcheck(self):
        user = users.get_current_user()
        if user:
            user = str(user)
            userok = db.GqlQuery("SELECT * FROM UserDB WHERE user = :1", user)
            results = userok.get()
            if results:
                if user == results.user:
                    authorized = True
                    print "match"
            else:
                self.redirect('/adduser')
                authorized = False
        else:
            authorized = False
            self.redirect('/addduser')
        return authorized

def UserDB_key(name = 'default'):
    return db.Key.from_path('users', name)

class UserDB(db.Model):
    user = db.StringProperty(required = True)
    companyname = db.StringProperty(required = True)

def input_key(name = 'default'):
    return db.Key.from_path('inputs', name)


class MainPage(InstrumentDataHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class AdduserPage(InstrumentDataHandler):

    def get(self):
        if self.authcheck():
            self.redirect('/input')
        user = users.get_current_user()
        self.render('adduser.html')

    def post(self):
        user = self.request.get('user')
        companyname = self.request.get('companyname')
        print user
        print companyname   
        s = UserDB(parent = UserDB_key(), user = user, companyname = companyname)
        s.put()

class Input(db.Model):
    frequency = db.FloatProperty(required = True)
    S11dB = db.FloatProperty(required = True)
    S12dB = db.FloatProperty(required = True)
    description = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def render(self):
        self._render_text = self.inputdata.replace('\n', '<br>')
        return render_str("post.html", p = self)

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
        
        #self.render("front.html")
        self.redirect('/data/' + description)
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/input', InputPage),
    ('/data/?', DataPage),
    ('/data/([a-zA-Z0-9-]+)', DataPage),
    ('/adduser', AdduserPage)
], debug=True)
