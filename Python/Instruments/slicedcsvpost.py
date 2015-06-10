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
f = itertools.islice(f, 18, 100)
sample_chunk = 10

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

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
    times = sorted(times, reverse=True)
    slicename = str("slice%sto%s" % (float(times[0]), float(times[-1])))
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':new}
    out = json.dumps(window)
    url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code



		
