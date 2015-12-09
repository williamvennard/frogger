#!/usr/bin/env python
"""Uploads CSV file as JSON object to searchdemo POST handler"""

import csv
import json
import requests

def rows_from_file(fname):
    f = open(fname)
    reader = csv.DictReader(f, fieldnames=("TIME", "CH1", "CH2", "CH3",
                                           "CH4"))
    reader = csv.DictReader(f,
                            fieldnames=("max_value", "min_value", "data",
                                        "pass_fail", "Start_TSE",
                                        "config_name", "pass_fail_type",
                                        "test_plan", "correction_frequency",
                                        "active_testplan_name")
                           )
    return [row for row in reader]

datarows = rows_from_file('../../DataFiles/powerMeterSample.1.csv')
outrows = json.dumps(datarows)
print "outrows =", outrows
#url = "https://fiberboardfreeway.appspot.com/searchdemo/upload"
url = "http://localhost:8080/searchdemo/upload"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
s = requests.session()
r = s.post(url, data=outrows, headers=headers)
print "r.reason=", r.reason
print "r.status_code=", r.status_code
