"""
This is the "main gradientone server" module.  

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
from google.appengine.api import taskqueue
from time import gmtime, strftime
from collections import OrderedDict
import numpy as np
import appengine_config
import decimate
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from string import maketrans
import testcomplete
import datamgmt
import testlibrary
import testanalyzer
import oscopedata
import testresultsdata
import bscopedata
import bscopedatadec
import search
import canvaspage
import testconfiginput
import testconfigoutput
import testsave
import instruments
import configoutput #importing is not working for this.  FIX IT!
import status
import testplansummary
import configinput
import bscopeconfig
import communitytests
import mainpage
import configlookup
import testmanager
import traceresultsdata
import exploremodestop
import exp_testconfiginput
import panelcontrol
import instlookup
import testlibrarytrace
import testlibrarytest
import onedb
from gradientone import InstrumentDataHandler

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

def query_to_dict(result):
    query_dict = [r.to_dict() for r in result]
    return query_dict


class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])




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


app = webapp2.WSGIApplication([
    ('/', mainpage.Handler),
    ('/help', mainpage.Handler),
    ('/adduser', AdduserPage),
    ('/listusers', ListUsersPage),
    ('/configlookup', configlookup.Handler),
    ('/instruments', instruments.Handler),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', instruments.Handler),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', instruments.Handler),
    ('/panelcontrol/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', panelcontrol.Handler),
    ('/configinput', configinput.Handler),
    ('/bscopeconfiginput', bscopeconfig.Handler),
    ('/configoutput/([a-zA-Z0-9-]+)', configoutput.Handler),
    ('/configoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', configoutput.Handler),
    ('/datamgmt/bscopedata/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', datamgmt.Handler),
    ('/testconfiginput', exp_testconfiginput.Handler),
    ('/testconfigoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testconfigoutput.Handler),
    ('/testplansummary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testplansummary.Handler),
    ('/testplansummary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testplansummary.Handler),
    ('/exploremodestop/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', exploremodestop.Handler),
    ('/community', communitytests.Handler),
    ('/communityprivate', communitytests.PrivateHandler),
    ('/saveposttotest', communitytests.SavePostToTest),
    ('/search', search.Handler),
    ('/status/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', status.Handler),
    ('/testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', testcomplete.Handler),
    ('/testresults', canvaspage.Handler),
    ('/testresults/([a-zA-Z0-9-]+)', testresultsdata.Handler),
    ('/testresults/([a-zA-Z0-9-]+.json)', canvaspage.Handler),
    ('/testresults/widgets/([a-zA-Z0-9-]+.json)', canvaspage.Handler),
    ('/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', testresultsdata.Handler),
    ('/testlibrary/([a-zA-Z0-9-]+)', testlibrary.Handler),
    ('/testlibrary/([a-zA-Z0-9-]+.json)', testlibrary.Handler),
    ('/testlibrary/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testlibrarytest.Handler),
    ('/testlibrary/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', testlibrarytest.Handler),
    ('/testlibrary/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testlibrarytrace.Handler),
    ('/testlibrary/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', testlibrarytrace.Handler),
    ('/testanalyzer/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testanalyzer.Handler),
    ('/oscopedata/([a-zA-Z0-9-]+)', oscopedata.Handler),
    ('/oscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', oscopedata.Handler),
    ('/bscopedata/([a-zA-Z0-9-]+)//([a-zA-Z0-9.-]+)', bscopedata.Handler),
    ('/bscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', bscopedata.Handler),
    ('/bscopedata/dec/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', bscopedatadec.Handler),
    ('/testsave', testsave.Handler),
    ('/upload/geturl', UploadURLGenerator),
    ('/upload/upload_file', FileUploadHandler),
    ('/upload/success',FileUploadSuccess),
    ('/upload/failure',FileUploadFailure),
    ('/testmanager', testmanager.Handler),
    ('/instlookup/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', instlookup.Handler),
    ('/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', traceresultsdata.Handler)
], debug=True)




# danger!!  don't say it unless you mean it:  db.delete(VNADB.all(keys_only=True))  # deletes entire table!!
