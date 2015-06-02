import csv
import itertools
import json
import requests
import time
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 100)
reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3"    , "CH4"))
def getKey(row):
    return float(row['TIME'])

datarows = [row for row in reader]
datarows = sorted(datarows,key=getKey)
window = {'config':{'TEK':'TODO'},'slicename':'18to100','data':datarows}
out = json.dumps(window)
#print "out =",out
#url = "https://fiberboardfreeway.appspot.com/oscopedata/tahoe-scope-2015-05-31-1500"
url = "http://localhost:8080/oscopedata/tahoe-scope-2015-05-31-1500"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=out, headers=headers)
print "r.reason=",r.reason
print "r.status_code=",r.status_code
