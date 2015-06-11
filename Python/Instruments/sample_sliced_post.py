import csv
import itertools
import json
import requests
import time

def key_to_string(k):
    s = ""
    if k < 0:
        s = "m"
        k = -k
    return s + str(k).replace('.','p')

def keys_to_slicename(first,last):
    return key_to_string(first) + "to" + key_to_string(last)
    
def getKey(row):
    return float(row['TIME'])

def rows_from_file(fname):
    f = open(fname)
    reader = csv.DictReader(f,fieldnames=("TIME","CH1","CH2","CH3","CH4"))
    return [row for row in reader]

def post_rows(hostname, dataname, instrument, config, slicename, datarows):
    window = {'config':config,'slicename':slicename,'data':datarows}
    out = json.dumps(window)
    if hostname.find('localhost') < 0:
        url = "https://%(hostname)s/%(dataname)s/%(instrument)s" % locals()
    else:
        url = "http://%(hostname)s/%(dataname)s/%(instrument)s" % locals()
        print "post_rows: use http for local testing. url=",url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=out, headers=headers)
    print "r.reason=%s,r.status=%s" % (r.reason,r.status_code)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def row_list_to_dict(rows):
    new_dict = {}
    for row in rows:
        k = row['TIME']
        new_dict[k] = row
    return new_dict

#hostname = 'gradientone-test.appspot.com'
#hostname = 'fiberboardfreeway.appspot.com'
hostname = 'localhost:8080'
dataname = 'oscopedata'
instrument = 'tahoe-scope-A'
datarows = rows_from_file('../../DataFiles/tekcsv/tek0012ALL.csv')
datastart = 17 # need better way to figure this out later
config = str(datarows[:datastart])
config = config[:450]  # todo: need way to compress config
datarows = sorted(datarows[datastart:], key=getKey)
datarows = datarows[:1000] # for testing. don't post the whole thing, yet.
howmany = len(datarows)
chunksize = int(0.01 * howmany)
if chunksize < 10:
    chunksize = howmany  # just take them all in one chunk
column_names = ['TIME', 'CH1', 'CH2', 'CH3', 'CH4']
for chunk in chunks(datarows, chunksize):
    first = float(chunk[0]['TIME'])
    last = float(chunk[-1]['TIME'])
    slicename = keys_to_slicename(first,last)
    row_dict = row_list_to_dict(chunk)
    post_rows(hostname, dataname, instrument, config, slicename, row_dict)

print "sample posts complete"
