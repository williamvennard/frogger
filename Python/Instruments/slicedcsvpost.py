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
from itertools import izip_longest
from itertools import izip

f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 49990, 50030)
sample_chunk = 10

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def slicename_creation(times):
    modified_time = []
    for time in times:
        modified_time.append(float(time))
    modified_time = sorted(modified_time, reverse=True)
    slicename = "slice%sto%s" % (modified_time[0], modified_time[-1])
    return slicename

def post_creation(window, slicename):
    out = json.dumps(window)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #url = "https://gradientone-test.appspot.com/oscopedata/amplifier/%s" % slicename
    url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code

out = grouper(f, sample_chunk, 0)
values = list(out)
keys = ['TIME', 'CH1', 'CH2', 'CH3', 'CH4']

for value in values:
    new = {}
    for item in value:
        if item != 0:
            item = item.strip()
            k = item.split(",")
        time = k[0]
        new[time] = dict(zip(keys,k))
    times = list(new.keys())
    slicename =  slicename_creation(times)
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':new}
    post_creation(window, slicename)


#https://gradientone-test.appspot.com/oscopedata/default-scope

		
