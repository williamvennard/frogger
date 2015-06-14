"""
This is the "slicedcsvpost" script.

It opens a file, slices the desired # of rows to transmit, then uses the
grouper function to 'chunk' the slice into amounts for a loop of HTTP POST.
"""
import csv
import itertools
import json
import requests
import time
import datetime
from time import gmtime, strftime
from itertools import izip_longest
from itertools import izip
from collections import OrderedDict

f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 58)
sample_chunk = 10
keys = ['TIME', 'CH1', 'CH2', 'CH3', 'CH4', 'TSE']

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def add_time_since_epoch(values):
    reconstructed_values = []
    for value in values:
        for item in value:
            if item !=0:
                item = item.strip()
                k = item.split(",")
            tse = time.time() + (float(k[0]))
            k.append(tse)
            reconstructed_values.append(k)
    return reconstructed_values

def slicename_creation(data_dict):
    slice_list = []
    for d in data_dict:
        slice_list.append(data_dict[d]['TSE'])
    slice_list = sorted(slice_list)
    slicename = "slice%sto%s" % (slice_list[0], slice_list[-1])
    return slicename

def post_creation(window, slicename):
    out = json.dumps(window)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #url = "https://gradientone-dev1.appspot.com/oscopedata/amplifier/%s" % slicename
    url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code

out = grouper(f, sample_chunk, 0)
values = list(out)
reconstructed_values = add_time_since_epoch(values)
new_data = grouper(reconstructed_values, sample_chunk, 0)
values = list(new_data)
for value in values:
    data_dict = {}
    for item in value:
        data_dict[item[0]] = dict(zip(keys, item))
    slicename = slicename_creation(data_dict)
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':data_dict}
    post_creation(window, slicename)   






