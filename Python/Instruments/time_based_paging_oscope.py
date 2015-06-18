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


def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def find_window(start_ms):
    if start_ms <=100:
        window =  '0-99'
        times = range(0,100)

    elif start_ms <=199:
        window = '100-199'
        times = range(100,200)

    elif start_ms <=299:
        window = '200-299'
        times = range(200,300)

    elif start_ms <=399:
        window = '300-399'
        times = range(300,400)

    elif start_ms <=499:
        window = '400-499'
        times = range(400,500)

    elif start_ms <=599:
        window = '500-599'
        times = range(500,600)

    elif start_ms <=699:
        window = '600-699'
        times = range(600,700)

    elif start_ms <=799:
        window = '700-799'
        times = range(700,800)

    elif start_ms <=899:
        window = '800-899'
        times = range(800,900)

    elif start_ms <=999:
        window = '900-999'
        times = range(900,1000)

    return window, times

def slicename_creation(tse):
    """creates slicenames based off time since epoch, rounded down to nearest 100 msec"""
    slicename = tse//100*100
    return slicename

def post_creation(stuffing):
    out = json.dumps(stuffing)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = "https://gradientone-test.appspot.com/oscopedata/amplifier/%s" % slicename
    #url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code


i = datetime.datetime.now()
start_ms = int(i.strftime('%f'))/1000
tse = dt2ms(i)
print 'time since epoch = ', tse
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 1018)
test_results = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
test_results = [row for row in test_results]
window = find_window(start_ms)[0]
times = find_window(start_ms)[1]
data_length = len(test_results)
delta_times = times[(start_ms-times[0])] - times[0]
stuffing = []


if start_ms + data_length < times[-1]:
    """stuffing routine for data contained in a single 100 msec window"""
    tr = ""
    z = (data_length+(start_ms-times[0]))
    for tr in test_results:
        new_dtms = dt2ms(i) + test_results.index(tr) 
        tr['DTE'] = new_dtms
        stuffing.append(tr)
    slicename = slicename_creation(tse)
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
    post_creation(window)



if start_ms + data_length > times[-1]:
    """stuffing routine for data that spills into adjacent 100msec window"""
    slicename = slicename_creation(tse)
    for tr in test_results:
        new_dtms = dt2ms(i) + test_results.index(tr) 
        tr['DTE'] = new_dtms
        if (test_results.index(tr) + start_ms)%100 == 0:
            window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
            post_creation(window)
            stuffing = []
            tr['DTE'] = new_dtms
            slicename = slicename_creation(new_dtms)
            stuffing.append(tr)
            continue
        stuffing.append(tr)
    slicename = slicename_creation(tr['DTE'])
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
    post_creation(window)



   




