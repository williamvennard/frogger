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
import searchdemo
import StringIO
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
import comments
from gradientone import InstrumentDataHandler
from onedb import ProfileDB
from onedb import UserDB
from onedb import company_key
from onedb import FileBlob
from onedb import BlobberDB
from onedb import Blobber_key
import measurements
import test_make_interface
import operatordata
import u2000_configinput
import u2000_testcomplete
import testops
import report_summary
import report_detail
import u2000_traceresultsdata
import u2000_testresultsdata
import urllib
import sys
from google.appengine.api import urlfetch
from encode import multipart_encode, MultipartParam
import view_testplan
import blob_selection
import blob_export

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


# def FileBlob_key(name = 'default'):
#     return db.Key.from_path('company_nickname', name)

# class FileBlob(db.Model):
#     blob_key = blobstore.BlobReferenceProperty(required=True)


class UploadURLGenerator(InstrumentDataHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload/upload_file')
        self.response.out.write(upload_url)
    def post(self):
        UploadURLGenerator.get(self)

class AggFileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0] 
            blob_key = upload.key()
            load = self.request.body
            load = load.split()
            load = load[4].split('=')
            load = load[1].rstrip('"')
            active_testplan_name = load.lstrip('"')
            dbfile = FileBlob(key_name = active_testplan_name, blob_key=blob_key)
            dbfile.put()
            str_form = str(blob_key)
            b = BlobberDB(b_key = str_form, key_name = active_testplan_name, parent = company_key())
            b.put()
            self.redirect('/upload/success')
        except:
            self.redirect('/upload_failure.html')

# def Blobber_key(name = 'default'):
#     return db.Key.from_path('company_nickname', name)

# class BlobberDB(DictModel):
#     b_key = db.StringProperty(required = True)

def incoming_blob_parser(value):
    headers = value[0].split(',')
    headers[-1] = headers[-1].rstrip()
    content = value[1].split(',')
    content[-1] = content[-1].rstrip()
    return headers, content

class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0] 
            blob_key = upload.key()
            load = self.request.body
            load = load.split()
            load = load[21].split('=')
            first_key = load[1]
            first_key = first_key.lstrip('"')
            first_key = first_key.rstrip('"')
            load = load[1].split(':')
            print 'key to db', first_key
            active_testplan_name = load[1].rstrip('"')
            config_name = load[0].lstrip('"')
            dbfile = FileBlob(key_name = first_key, test_batch = first_key, blob_key=blob_key, parent = company_key())
            dbfile.put()
            key = db.Key.from_path('BlobberDB', active_testplan_name, parent = company_key())
            new_blob_key = db.get(key)
            if new_blob_key:
                print 'something there'
                newkey = new_blob_key.b_key
                blob_reader = blobstore.BlobReader(blob_key)
                value = blob_reader.readlines()
                input_to_blob = incoming_blob_parser(value)
                tmp = StringIO.StringIO()
                writer = csv.writer(tmp)
                writer.writerow(input_to_blob[0])
                writer.writerow(input_to_blob[1])
                print 'reading original'
                new_blob_reader = blobstore.BlobReader(newkey)
                new_lines = new_blob_reader.readlines()
                headers = new_lines[0].split(',')
                headers[-1] = headers[-1].rstrip()
                for item in new_lines[1:]:
                    item = item.split(',')
                    item[-1] = item[-1].rstrip()
                    writer.writerow(item)
                contents = tmp.getvalue()
                tmp.close()
                blobstore.delete(newkey)
                new_url =  blobstore.create_upload_url('/upload_agg/upload_file')
                params = []
                params.append(MultipartParam(
                            "FileItem1",
                            filename=active_testplan_name,
                            filetype='text/plain',
                            value=contents))
                payloadgen, headers = multipart_encode(params)
                payload = str().join(payloadgen)
                result = urlfetch.fetch(
                            url=new_url,
                            payload=payload,
                            method=urlfetch.POST,
                            headers=headers,
                            deadline=10)
            else:
                print 'nothing found'
                blob_reader = blobstore.BlobReader(blob_key)
                value = blob_reader.readlines()
                input_to_blob = incoming_blob_parser(value)
                tmp = StringIO.StringIO()
                writer = csv.writer(tmp)
                writer.writerow(input_to_blob[0])
                writer.writerow(input_to_blob[1])
                contents = tmp.getvalue()
                tmp.close()
                str_form = str(blob_key)
                b = BlobberDB(b_key = str_form, key_name = active_testplan_name, parent = company_key())
                b.put()
                key = db.Key.from_path('BlobberDB', active_testplan_name, parent = company_key())
                new_blob_key = db.get(key)
                newkey = new_blob_key.b_key
                blob_reader = blobstore.BlobReader(newkey)
                value = blob_reader.readlines()
                new_url =  blobstore.create_upload_url('/upload_agg/upload_file')
                params = []
                params.append(MultipartParam(
                            "FileItem1",
                            filename=active_testplan_name,
                            filetype='text/plain',
                            value=contents))
                payloadgen, headers = multipart_encode(params)
                payload = str().join(payloadgen)
                result = urlfetch.fetch(
                            url=new_url,
                            payload=payload,
                            method=urlfetch.POST,
                            headers=headers,
                            deadline=10)
            self.redirect('/upload/success')
        except:
            self.redirect('/upload_failure.html')


class FileUploadSuccess(InstrumentDataHandler):
    def get(self):
        self.response.out.write("File Upload Successful")

class FileUploadFailure(InstrumentDataHandler):
    def get(self):
        self.response.out.write("File Upload Failed")


class FileNotFound(InstrumentDataHandler):
    """Handler for FileNotFound"""
    def get(self):
        self.error(404)
        self.response.out.write("404 Error: File not found")


app = webapp2.WSGIApplication([
    ('/', mainpage.Handler),
    ('/404', FileNotFound),
    ('/adduser', profile.AdduserPage),
    ('/admin/adduser', profile.AdminAddUser),
    ('/admin/editusers', profile.AdminEditUsers),
    ('/blob_export/([a-zA-Z0-9-]+)', blob_export.Handler),
    ('/blob_selection', blob_selection.Handler),
    ('/bscopeconfiginput', bscopeconfig.Handler),
    ('/bscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', bscopedata.Handler),
    ('/bscopedata/([a-zA-Z0-9-]+)//([a-zA-Z0-9.-]+)', bscopedata.Handler),
    ('/bscopedata/dec/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', bscopedatadec.Handler),
    ('/comments', comments.Handler),
    ('/community', communitytests.Handler),
    ('/communityprivate', communitytests.PrivateHandler),
    ('/configinput', configinput.Handler),
    ('/configlookup', configlookup.Handler),
    ('/configoutput/([a-zA-Z0-9-]+)', configoutput.Handler),
    ('/configoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', configoutput.Handler),
    ('/datamgmt/bscopedata/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', datamgmt.Handler),
    ('/exploremodestop/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', exploremodestop.Handler),
    ('/help', mainpage.Handler),
    ('/instlookup/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', instlookup.Handler),
    ('/instruments', instruments.Handler),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', instruments.Handler),
    ('/instruments/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', instruments.Handler),
    ('/listusers', profile.ListUsersPage),
    ('/oauthtest/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', status.OAuthHandler),
    ('/operator/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', operatordata.NewHandler),
    ('/operator/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', operatordata.Handler),
    ('/operator/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/run', operatordata.RunTest),
    ('/oscopedata/([a-zA-Z0-9-]+)', oscopedata.Handler),
    ('/oscopedata/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)', oscopedata.Handler),
    ('/panelcontrol/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', panelcontrol.Handler),
    ('/profile', profile.Handler),
    ('/report_summary/([a-zA-Z0-9.-]+)',  report_summary.Handler),
    ('/report_summary/report_detail/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)',  report_detail.Handler),
    ('/saveposttotest', communitytests.SavePostToTest),
    ('/scriptconfig', scriptconfig.Handler),
    ('/search', searchdemo.Handler),
    ('/searchdemo', searchdemo.Handler),
    ('/searchdemo/', searchdemo.Handler),
    ('/searchdemo/upload', searchdemo.Handler),
    ('/status/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', status.Handler),
    ('/temp_testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', temp_testcomplete.Handler),
    ('/test_make_interface', test_make_interface.Handler),    
    ('/testanalyzer/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testanalyzer.Handler),
    ('/testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', testcomplete.Handler),
    ('/testconfiginput', exp_testconfiginput.Handler),
    ('/testconfigoutput/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testconfigoutput.Handler),
    ('/testlibrary', testlibrary.Handler),
    ('/testlibrary/([a-zA-Z0-9-]+)', testlibrary.Handler),
    ('/testlibrary/([a-zA-Z0-9-]+.json)', testlibrary.JSON_Handler),
    ('/testlibrary/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testlibrarytest.Handler),
    ('/testlibrary/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', testlibrarytest.JSON_Handler),
    ('/testlibrary/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', testlibrarytest.TestResultsSet),
    ('/testlibrary/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testlibrarytrace.Handler),
    ('/testlibrary/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.json)', testlibrarytrace.Handler),
    ('/testmanager', testmanager.Handler),
    ('/testops', testops.Handler),
    ('/testplansummary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testplansummary.Handler),
    ('/testplansummary/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)', testplansummary.Handler),
    ('/testresults', canvaspage.Handler),
    ('/testresults/([a-zA-Z0-9-]+)', testresultsdata.Handler),
    ('/testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', testresultsdata.Handler),
    ('/testresults/([a-zA-Z0-9-]+.json)', canvaspage.Handler),
    ('/testresults/widgets/([a-zA-Z0-9-]+.json)', canvaspage.Handler),
    ('/testsave', testsave.Handler),
    ('/traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', traceresultsdata.Handler),
    ('/u2000_configinput', u2000_configinput.Handler),
    ('/u2000_testcomplete/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000_testcomplete.Handler),
    ('/u2000_testresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000_testresultsdata.Handler),
    ('/u2000_traceresults/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000_traceresultsdata.Handler),
    ('/u2000_update_results', u2000_testcomplete.UpdateResults),
    ('/u2000data/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', u2000data.Handler),
    ('/upload/failure',FileUploadFailure),
    ('/upload/geturl', UploadURLGenerator),
    ('/upload/success',FileUploadSuccess),
    ('/upload/upload_file', FileUploadHandler),
    ('/upload_agg/upload_file', AggFileUploadHandler),
    ('/view_testplan/([a-zA-Z0-9-]+)/([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)', view_testplan.Handler),
], debug=True)




# danger!!  don't say it unless you mean it:  db.delete(VNADB.all(keys_only=True))  # deletes entire table!!
