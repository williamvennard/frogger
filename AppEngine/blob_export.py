from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import query_to_dict
import json
import itertools
import jinja2
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
from onedb import FileBlob
from onedb import company_key
from onedb import BlobberDB
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import StringIO
import csv
from encode import multipart_encode, MultipartParam
from google.appengine.api import urlfetch
from pydblite import Base
import urllib


class Handler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, input_resource):
        print input_resource
        resource = str(urllib.unquote(input_resource))
        key = db.Key.from_path('BlobberDB', input_resource, parent = company_key())
        filename = str(input_resource), + '.csv'
        print 'key =', key
        new_blob_key = db.get(key)
        print 'new blob key = ', new_blob_key
        newkey = new_blob_key.b_key
        print 'newkey =', newkey
        blob_info = blobstore.BlobInfo.get(newkey)
        print blob_info
        self.send_blob(blob_info,save_as=filename)


