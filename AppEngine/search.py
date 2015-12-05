from gradientone import InstrumentDataHandler
from gradientone import author_creation
from gradientone import query_to_dict
import json
import itertools
import jinja2
import webapp2
import time
import datetime
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
import appengine_config
from onedb import FileBlob
from onedb import company_key
from onedb import FileBlob
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import StringIO
import csv
from encode import multipart_encode, MultipartParam
from google.appengine.api import urlfetch
from pydblite import Base

class Handler(InstrumentDataHandler):
    def post(self):
        params = self.request.body
        params = params.split('=')
        key = params[1].split('&')
        key = key[0]
        search_input = params[2]
        print search_input
        print key
        output = memcache.get(key)
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
        #reader = csv.reader(contents, delimiter=';')
        reader = csv.reader(StringIO.StringIO(contents))
        pydb = Base('temp', save_to_file=False)
        # create new base with field names
        pydb.create('Start_TSE', 'correction_frequency', 'config_name', 'max_value', 'min_value', 'offset', 'pass_fail_type', 'test_plan', 'data',  'active_testplan_name', 'data', 'pass_fail')
        new_counter = 0
        for row in reader:
            if new_counter != 0:
                pydb.insert(Start_TSE = row[0], 
                    correction_frequency = row[1], 
                    config_name = row[2], 
                    max_value= row[3], 
                    min_value = row[4], 
                    offset = row[5], 
                    pass_fail_type = row[6], 
                    test_plan = row[7],
                    data = row[8],
                    active_testplan_name = row[9],
                    pass_fail = row[10],
                                     )
            else:
                pass
            new_counter +=1
        records = pydb(active_testplan_name="Production")
        print records
        for r in records:
            print r