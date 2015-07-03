"""
This is the "time_based_paging_oscope" script.

It opens a file & slices the desired # of rows to transmit.  It 
subseuqently looks for appropriate time windows to slot the data
in.

It adds the # of msec since the epoch as the DTE entry in 
the data dictionary.

"""

import time
import datetime 
import math
import csv
import itertools
import json
import requests
from itertools import izip_longest
from itertools import izip
from requests_toolbelt.multipart.encoder import MultipartEncoder

def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def post_creation(slicename, stuffing):
    window = {'config':{'Sample_Size':data_length, 'Sample_Rate(Hz)':sample_rate, 'Slice_Size(msec)':slice_size,'slicename':slicename},'data':stuffing, 'start_tse':start_tse}
    out = json.dumps(window)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #url = "https://gradientone-test.appspot.com/oscopedata/LED/%s" % slicename
    url = "http://localhost:18080/oscopedata/LED/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    #print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code

def send_blob():
    #blob_url = requests.get("https://gradientone-test.appspot.com/upload/geturl")
    blob_url = requests.get("http://localhost:18080/upload/geturl")
    m = MultipartEncoder(
        fields={'field0': ('tek0012ALL', open('../../DataFiles/tekcsv/tek0012ALL.csv', 'rb'), 'text/plain')}
        )
    b = requests.post(blob_url.text, data = m, headers={'Content-Type': m.content_type})
    print "b.reason=",b.reason
    print "b.status_code=",b.status_code

i = datetime.datetime.now()
start_tse = roundup(dt2ms(i))
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
z = f
f = itertools.islice(f, 18, 20)
test_results = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
test_results = [row for row in test_results]
data_length = len(test_results)
stuffing = []
sample_rate = 100 # fixed value from Tek csv files (Hz).  1 sample every 10 miliseconds.
slice_size = 100 # miliseconds
sample_per_slice = int((float(sample_rate)/1000)*float(slice_size))
for i in range(0, data_length, sample_per_slice):
    chunk = str(test_results[i:i + sample_per_slice])
    slicename = start_tse + i*sample_per_slice
    stuffing = chunk
    post_creation(slicename, stuffing)    
send_blob()





