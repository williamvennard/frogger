import os
import webapp2
import jinja2
import json
import datetime
import re
import csv
import itertools
from time import gmtime, strftime
import collections
import hashlib
import time, threading
from google.appengine.ext import db
from google.appengine.api import users
import threading;
import requests


def work():
	threading.Timer(5, work).start(); 
	print "hi"
	r = requests.get('http://fiberboardfreeway.appspot.com/config.json')
	print r
	config_var = r.text
	print config_var
	if config_var[0] == 'start':
		self.redirect('oscope.json')
		#f = open('tek0012ALL.csv')
        #f = itertools.islice(f, 18, 100)
        #reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
        #out = json.dumps([row for row in reader])
        #p = requests.post("http://fiberboardfreeway.appspot.com/oscope.json", data=out)  

work();



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

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

#class OscopeData(db.Model):
#   time = db.FloatProperty(required = True)
#    ch1 = db.FloatProperty(required = True)
#    ch2 = db.FloatProperty(required = True)
#    ch3 = db.FloatProperty(required = True)
#    ch4 = db.FloatProperty(required = True)

#def Oscope_key(name = 'default'):
#    return db.Key.from_path('oscopedata', name)

class OscopePage(InstrumentDataHandler):
    def get(self):
    	print "oscope handler"
        f = open('tek0012ALL.csv')
        f = itertools.islice(f, 18, 100)
        reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
        out = json.dumps([row for row in reader])
        self.response.write(out)
        
        #for row in reader:
            #r = OscopeData(parent = Oscope_key(), time = TIME, ch1 = CH1, ch2 = CH2, ch3 = CH3, ch4 = CH4)
            #r.put()



#class MainHandler(webapp2.RequestHandler):
#    def get(self):
#        self.response.write('Hello world!')
#
#        r=requests.post("https://accounts.google.com/o/oauth2/token")
#                           headers={
#                               'content-type':'application/x-www-form-urlencoded'},
#                           data={
#                   		    'client_id':'1023941599436-v1mlfpv9ukdv8lfnhkp4snp10f6rc537.apps.googleusercontent.com',
#                               'client_secret':'wiLNYGbRIMRKOq_v_OM0yjN3',
#                               'redirect_uri':'http://localhost/etc'})



app = webapp2.WSGIApplication([ 
    ('/oscope.json', OscopePage),
], debug=True)