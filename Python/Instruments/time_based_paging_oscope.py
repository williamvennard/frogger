"""
This is the "time_based_paging_oscope" script.

It opens a file & slices the desired # of rows to transmit.  It 
subseuqently looks for appropriate time windows to slot the data
in, then pads with leading or trailing zeros as necessary to 
fill in 100 msec of data.

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

def slicename_creation(i, window, tr, start_ms):
    """creates slicenames with "%Y-%m-%d-%H-%M-%S-" followed by msec window"""
    t = datetime.datetime.strftime(i, "%Y-%m-%d-%H-%M-%S-")
    if tr == "":
        slicename = "%s%s" % (t, window)
    else:
        new_dtms = dt2ms(i) + test_results.index(tr) 
        new_dtms = datetime.datetime.fromtimestamp(new_dtms/1000.0)
        start_ms = int(new_dtms.strftime('%f'))/1000
        start_ms = start_ms - 1
        window = find_window(start_ms)[0]
        t = datetime.datetime.strftime(new_dtms, "%Y-%m-%d-%H-%M-%S-")
        slicename = "%s%s" % (t, window) 
    return slicename

def post_creation(stuffing):
    out = json.dumps(stuffing)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = "https://gradientone-dev1.appspot.com/oscopedata/amplifier/%s" % slicename
    #url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code


i = datetime.datetime.now()
start_ms = int(i.strftime('%f'))/1000
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 118)
test_results = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
test_results = [row for row in test_results]
window = find_window(start_ms)[0]
times = find_window(start_ms)[1]
data_length = len(test_results)
delta_times = times[(start_ms-times[0])] - times[0]
stuffing = []


if start_ms + data_length < times[-1]:
    """padding & stuffing routine for data contained in a signle 100 msec window"""
    tr = ""
    z = (data_length+(start_ms-times[0]))
    for t in times[:(delta_times)]:
        beginning =  int(i.strftime('%s'))*1000
        new_dtms = beginning + t
        stuffing.append({'CH1':'0', "CH2": "0", "CH3": "0", "CH4": "0", "TIME": "0", "DTE": new_dtms})
    for tr in test_results:
        new_dtms = dt2ms(i) + test_results.index(tr) 
        tr['DTE'] = new_dtms
        stuffing.append(tr)
    for t in times[z:]:
        new_dtms = test_results[0]['DTE'] + t - start_ms 
        stuffing.append({'CH1':'0', "CH2": "0", "CH3": "0", "CH4": "0", "TIME": "0", "DTE": new_dtms})
    slicename = slicename_creation(i, window, tr, start_ms)
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
    post_creation(window)
    print "mini-me posted"


if start_ms + data_length > times[-1]:
    """padding & slicing routine data that spills into adjacent 100msec window"""
    for t in times[:delta_times]:
        beginning =  int(i.strftime('%s'))*1000
        new_dtms = beginning + t
        stuffing.append({'CH1':'0', "CH2": "0", "CH3": "0", "CH4": "0", "TIME": "0", "DTE": new_dtms})
    for tr in test_results:
        new_dtms = dt2ms(i) + test_results.index(tr) 
        tr['DTE'] = new_dtms
        if (test_results.index(tr) + start_ms)%100 == 0:
            slicename = slicename_creation(i, window, tr, start_ms)
            window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
            post_creation(window)
            stuffing = []
            tr['DTE'] = new_dtms
            stuffing.append(tr)
            continue
        stuffing.append(tr)
    last_stuffing = stuffing
    fl = len(last_stuffing)
    for t in times[fl:]:
        new_dtms = test_results[-1]['DTE'] + t - start_ms +1
        last_stuffing.append({'CH1':'0', "CH2": "0", "CH3": "0", "CH4": "0", "TIME": "0", "DTE": new_dtms})
    slicename = slicename_creation(i, window, tr, start_ms)
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
    post_creation(window)



   




