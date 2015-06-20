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

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def slicename_creation(x):
    """creates slicenames based off time since epoch, rounded down to nearest 100 msec"""
    slicename = x//100*100
    return slicename

def post_creation(slicename, stuffing):
    window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
    out = json.dumps(window)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = "https://gradientone-test.appspot.com/oscopedata/amplifier/%s" % slicename
    #url = "http://localhost:18080/oscopedata/amplifier/%s" % slicename
    r = requests.post(url, data=out, headers=headers)
    print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code

i = datetime.datetime.now()
tse = dt2ms(i)
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 118)
test_results = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3", "CH4"))
test_results = [row for row in test_results]
data_length = len(test_results)

new_dtms = tse
stuffing = []

def end_creation(new_dtms):
    if str(new_dtms)[-2:] == '00':
        new_dtms = new_dtms + 1
    end = int(roundup(new_dtms))
    return end


for i in range(0, data_length, 10):

    chunk = test_results[i:i + 10]
    end = end_creation(new_dtms)
    slicename = slicename_creation(new_dtms)
    
    
    for tr in chunk:
        new_dtms =  int(tse - (-500.00 - float(tr['TIME']))*1000)
        tr['DTE'] = new_dtms
        if float(tr['DTE']) > end:
            post_creation(slicename, stuffing)
            stuffing = []
            slicename = slicename_creation(new_dtms)  
            stuffing.append(tr)
            end = end_creation(new_dtms)
            continue
        stuffing.append(tr)
    slicename = slicename_creation(new_dtms)
    post_creation(slicename, stuffing)
    stuffing = []
        

            


        


       
            

        



   




