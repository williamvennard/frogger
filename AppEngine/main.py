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
import profile
import scriptconfig
import u2000data
import temp_testcomplete
from gradientone import InstrumentDataHandler
from onedb import ProfileDB
from onedb import UserDB
import measurements
import test_make_interface
import operatordata
import u2000_configinput
import u2000_testcomplete
import report_summary
import report_detail

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
        self.admincheck()
        users = db.GqlQuery("SELECT * FROM ProfileDB WHERE company_nickname = 'GradientOne'").fetch(None)
        print "ListUsersPage:get: users =",users
        if len(users) > 0:
            self.render('listusers.html',company=users[0].company_nickname,
                        users=users)
        else:
            self.render('listusers.html',company="new company?",
                        users=users)
    def post(self):
        email = self.request.get('user_email')
        q = ProfileDB.all().filter("email =", email)
        profile = q.get()

        group = self.request.get('group')
        profile.groups.append(group)
        profile.put()

        group_to_delete = self.request.get('group_to_delete')
        profile.groups.remove(group_to_delete)
        profile.put()
        profile.groups = filter(None, profile.groups)
        profile.put()

        self.redirect('/listusers')


class AdduserPage(InstrumentDataHandler):
    def get(self):
        u = users.get_current_user()
        if not u:
            self.redirect('/')
            return

        # check for admin, if fails then redirects to auth error
        self.admincheck()
        
        admin_email = u.email()
        self.render('adduser.html')

    def post(self):
        email = self.request.get('email')
        companyname = self.request.get('companyname')
        name = self.request.get('name')
        # TODO - handle spaces in companyname
        s = ProfileDB(email = email, 
                      company_nickname = companyname, 
                      name = name)
        s.put()
        checked_box = self.request.get("admin")
        if checked_box:
            s.admin = True
            print s.admin
        else:
            s.admin = False
            print s.admin
        if not s.bio:
            s.bio = "No bio entered yet."
        s.put()
        self.redirect('/profile')

class FileNotFound(InstrumentDataHandler):
    """Handler for FileNotFound"""
    def get(self):
        self.error(404)
        self.response.out.write("404 Error: File not found")


app = webapp2.WSGIApplication([
    ('/', mainpage.Handler),
    ('/help', mainpage.Handler),
    ('/adduser', AdduserPage),
    ('/listusers', ListUsersPage),
    ('/profile', profile.Handler),
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
    ('/testconfiginput', testconfiginput.Handler),
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
    ('/scriptconfig', scriptconfig.Handler),
    ('/instlookup/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', instlookup.Handler),
    ('/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', traceresultsdata.Handler),
    ('/u2000data/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000data.Handler),
    ('/temp_testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', temp_testcomplete.Handler),
    ('/test_make_interface', test_make_interface.Handler),
    ('/operator/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', operatordata.Handler),
    ('/404', FileNotFound),
    ('/u2000_configinput', u2000_configinput.Handler),
    ('/u2000_testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000_testcomplete.Handler),
    ('/report_summary/([a-zA-Z0-9.-]+)',  report_summary.Handler),
    ('/report_summary/report_detail/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)',  report_detail.Handler)
], debug=True)




# danger!!  don't say it unless you mean it:  db.delete(VNADB.all(keys_only=True))  # deletes entire table!!
