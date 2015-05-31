import json
import requests
url = "https://fiberboardfreeway.appspot.com/testnuc"
#url = "http://localhost:8080/testnuc"
data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print "dir(r)=",dir(r)
print "r.reason=",r.reason
print "r.status_code=",r.status_code
