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
from profile import get_profile_cookie
import collections


def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)


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
        profile = get_profile_cookie(self)
        #if not self.authcheck():
         #   return
        rows = db.GqlQuery("SELECT * FROM FileBlob")
        print rows
        self.render('new_blob_selection.html', rows = rows, profile = profile)
    def post(self):
        profile = get_profile_cookie(self)
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
        output = []
        for test_batch in list_of_inputs:
            key = db.Key.from_path('FileBlob', test_batch, parent = company_key())
            new_blob_key = db.get(key)
            newkey = new_blob_key.blob_key
            blob_reader = blobstore.BlobReader(newkey)
            new_lines = blob_reader.readlines()
            headers = new_lines[0].split(',')
            headers[-1] = headers[-1].rstrip()
            for item in new_lines[1:]:
                if counter == 0:
                    writer.writerow(headers)                        
                item = item.split(',')
                item[-1] = item[-1].rstrip()
                print item
                if item[11] == 'N/A':
                    item[8] = 'N/A'
                    item[7] = 'N/A'
                writer.writerow(item)
            input_dictionary = dict(zip(headers, item))
            counter += 1
            output.append(input_dictionary)
        contents = tmp.getvalue()
        tmp.close()
        name_time = str(dt2ms(datetime.datetime.now()))
        newname = author + name_time
        key = newname
        final_output = []
        for entry in output:
            print entry
            temp_dict = collections.OrderedDict()
            del entry['test_plan']
            temp_dict['start_time'] = entry['Start_TSE']
            temp_dict['correction_frequency(Hz)'] = entry['correction_frequency(Hz)']
            temp_dict['config_name'] = entry['config_name']
            temp_dict['measurement_source'] = entry['measurement_source']
            temp_dict['max_value'] = entry['max_value']
            temp_dict['min_value'] = entry['min_value']
            temp_dict['offset(dBm)'] = entry['offset(dBm)']
            temp_dict['pass_fail_type'] = entry['pass_fail_type']
            temp_dict['data(dBm)'] = entry['data(dBm)']
            temp_dict['active_testplan_name'] = entry['active_testplan_name']
            temp_dict['hardware_name'] = entry['hardware_name']
            temp_dict['pass_fail'] = entry['pass_fail']
            final_output.append(temp_dict)
        memcache.set(key, final_output)
        self.render('blob_analyzer.html', result = final_output, 
            download_key = newname, profile = profile)


