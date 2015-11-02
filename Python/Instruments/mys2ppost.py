import csv
import itertools
import json
import requests
import time
from mytouchstone import Touchstone

touch = Touchstone('../../DataFiles/S2P/ERA_1_32mA_Minus45.S2P')
print touch.parse()

out = touch.make_json()


#config = {'config': 'to do', out}



#url = "https://gradientone-prod.appspot.com/vnadata/tahoe-vna-2015-06-02-1600"
url = "http://localhost:18080/vnadata/tahoe-vna-2015-06-02-1600"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


#window = {'config':{'TEK':'TODO'},'slicename':'18to100','data':[row for row in reader]}
#out = json.dumps(window)
#print "out =",out
start_time = time.time()
r = requests.post(url, data=out, headers=headers)
print "dir(r)=",dir(r)
print "r.reason=",r.reason
print "r.status_code=",r.status_code


total_time = time.time() - start_time

print "the total time took %f seconds" % total_time

