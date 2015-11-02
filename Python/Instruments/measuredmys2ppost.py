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
out_content = json.loads(out)
out_data = out_content['data']

keys = list(out_data.keys())


#url = "https://gradientone-test.appspot.com/vnadata/tahoe-vna-2015-06-02-1600"
url = "http://localhost:18080/vnadata/tahoe-vna-2015-06-02-1600"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

start_time = time.time()
for k in keys[:50]:
	

#window = {'config':{'TEK':'TODO'},'slicename':'18to100','data':[row for row in reader]}
#out = json.dumps(window)
#print "out =",out

	start_put_time = time.time()
	r = requests.post(url, data=out_data[k], headers=headers)
	print "dir(r)=",dir(r)
	print "r.reason=",r.reason
	print "r.status_code=",r.status_code
	end_put_time = time.time()
	put_time = end_put_time - start_put_time
	print put_time

total_time = time.time() - start_time
print total_time
print "the total time took %f seconds" % total_time

