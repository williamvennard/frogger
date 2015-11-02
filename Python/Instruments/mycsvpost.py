import csv
import itertools
import json
import requests
import time
#f = open('../../DataFiles/tekcsv/default_scope.csv')
f = open('../../DataFiles/tekcsv/tek0012ALL.csv')
f = itertools.islice(f, 18, 100)
reader = csv.DictReader(f, fieldnames = ("TIME", "CH1", "CH2", "CH3"    , "CH4"))
window = {'config':{'TEK':'TODO'},'slicename':'18to100','data':[row for row in reader]}
out = json.dumps(window)
print "out =",out
#url = "https://gradientone-test.appspot.com/oscopedata/default-scope"
url = "http://localhost:18080/oscopedata/default-scope/18to100"
#data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=out, headers=headers)
#print "dir(r)=",dir(r)
print "r.reason=",r.reason
print "r.status_code=",r.status_code
