#!/usr/bin/env python
"""Uploads CSV file as JSON object to searchdemo POST handler"""

import csv
import json
import requests
import sys

def rows_from_file(fname):
    f = open(fname)
    if '.1.' in fname:
        fieldnames=("max_value", "min_value", "data", "pass_fail", "Start_TSE",
                    "config_name", "pass_fail_type", "test_plan",
                    "correction_frequency", "active_testplan_name")
    else:
        fieldnames=("start_time","correction_frequency(Hz)","config_name",
                    "measurement_source","max_value","min_value","offset(dBm)",
                    "pass_fail_type","data(dBm)","active_testplan_name",
                    "hardware_name","pass_fail")
    reader = csv.DictReader(f, fieldnames=fieldnames)
    return [row for row in reader]

#datarows = rows_from_file('../../DataFiles/powerMeterSample.1.csv')
datarows = rows_from_file('../../DataFiles/powerMeterSample.2.csv')
outrows = json.dumps(datarows)
print "outrows =", outrows

if len(sys.argv) > 1:
   hostname = sys.argv[1]
   if hostname == "localhost":
       url = "http://localhost:8080/searchdemo/upload"
   elif hostname[:9] == "localhost":
       url = "http://" + hostname + "/searchdemo/upload"
   else:
       url = "https://" + hostname + "/searchdemo/upload"
else:
   url = "https://fiberboardfreeway.appspot.com/searchdemo/upload"
   #url = "http://localhost:8080/searchdemo/upload"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
s = requests.session()
r = s.post(url, data=outrows, headers=headers)
print "r.reason=", r.reason
print "r.status_code=", r.status_code
