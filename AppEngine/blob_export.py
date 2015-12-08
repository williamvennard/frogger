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
    def get(self, key):
        output = memcache.get(key)
        headers = self.response.headers
        headers['Content-Type'] = 'text/csv'
        headers['Content-Disposition'] =  'attachment; filename=' + key + '.csv'
        tmp = StringIO.StringIO()
        writer = csv.writer(tmp)
        counter = 0
        for item in output:
            if counter == 0:
                writer.writerow(item.keys())
                writer.writerow(item.values())
            else:
                writer.writerow(item.values()) 
            counter +=1
        contents = tmp.getvalue()
        tmp.close()
        self.response.out.write(contents)



