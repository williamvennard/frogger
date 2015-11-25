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
from onedb import FileBlob
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import StringIO
import csv
from encode import multipart_encode, MultipartParam
from google.appengine.api import urlfetch
from pydblite import Base


def existing_blob_parser(headers, item):
    new_rows = []
    entry = item.split('"')
    first = entry[0].split(',')
    del first[-1]
    last = entry[2].split(',')
    del last[0]
    new_rows.append(first[0])
    new_rows.append(first[1])
    new_rows.append(entry[1])
    new_rows.append(last[0])
    new_rows.append(last[1])
    new_rows.append((last[2].rstrip()))
    input_dictionary = dict(zip(headers, new_rows))
    return input_dictionary

class Handler(InstrumentDataHandler):
    def get(self):
        #if not self.authcheck():
         #   return
        rows = db.GqlQuery("SELECT * FROM FileBlob")
        print rows
        self.render('new_blob_selection.html', rows = rows)
    def post(self):
        author = 'nedwards'
        #author = author_creation()
        config_data = self.request.body
        config_data = config_data.split('test_batch')
        list_of_inputs = []
        del config_data[0]
        for item in config_data:
            temp = item.lstrip('=')
            temp = temp.rstrip('&')
            temp = temp.replace('%3A', ':')
            list_of_inputs.append(temp)
        counter = 0
        tmp = StringIO.StringIO()
        writer = csv.writer(tmp)
        for test_batch in list_of_inputs:
            key = db.Key.from_path('FileBlob', test_batch, parent = company_key())
            new_blob_key = db.get(key)
            newkey = new_blob_key.blob_key
            blob_reader = blobstore.BlobReader(newkey)
            new_lines = blob_reader.readlines()
            headers = new_lines[0].split(',')
            headers[-1] = headers[-1].rstrip()
            print headers
            for item in new_lines[1:]:
                if counter == 0:
                    writer.writerow(headers)                        
                item = item.split(',')
                item[-1] = item[-1].rstrip()
                print item
                writer.writerow(item)
            counter += 1
        contents = tmp.getvalue()
        tmp.close()
        reader = csv.reader(StringIO.StringIO(contents))
        pydb = Base('temp', save_to_file=False)
        # create new base with field names
        pydb.create('Start_TSE', 'config_name', 'test_plan', 'active_testplan_name', 'data', 'max_value', 'min_value', 'pass_fail', 'pass_fail_type', 'correction_frequency')
        new_counter = 0
        for row in reader:
            if new_counter != 0:
                pydb.insert(max_value = row[0],
                                     min_value = row[1],
                                     data = row[2],
                                     pass_fail = row[3],
                                     Start_TSE = row[4],
                                     config_name= row[5],
                                     pass_fail_type = row[6], 
                                     test_plan = row[7],
                                     correction_frequency = row[8],
                                     active_testplan_name = row[9],
                                     )
            else:
                pass
            new_counter +=1
        records = pydb(active_testplan_name="Senator")
        print records



