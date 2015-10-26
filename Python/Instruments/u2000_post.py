"""
The bscopepost module supplies one class, BitScope.  For example,

>>> from bscopepost import BitScope
>>> bits = BitScope(acq_dict)
>>> bits.transmit()
"""

import time
import datetime 
import math
import itertools
import json
import requests
import os, sys, stat
import csv
import grequests
#import urllib3 
#from urllib3.poolmanager import PoolManager
#from requests_toolbelt.multipart.encoder import MultipartEncoder

class agilentu2000:
    """Send script config to server.
    """
    global COMPANYNAME
    global HARDWARENAME
    COMPANYNAME = 'Acme'
    HARDWARENAME = 'MSP'

    def __init__(self, u2000_test_results, s):
        self.u2000_test_results = u2000_test_results
        self.s = s

    def post_creation_data(self, i_settings, stuffing, start_tse, parent, config_name, active_testplan_name, test_plan) :
        s = self.s
        window_u2000 = {'i_settings':i_settings, 'cha':stuffing, 'start_tse':start_tse, 'test_plan':test_plan, 'testplan_name':active_testplan_name}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #url_u = "http://localhost:18080/u2000data/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
        url_u = "https://gradientone-test.appspot.com/u2000data/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
        out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
        r = s.post(url_u, data=out_u2000, headers=headers)
        #print "dir(r)=",dir(r)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code

    def transmitraw(self):
        parent = 'raw'
        test_results = self.u2000_test_results['data']
        i_settings = self.u2000_test_results['i_settings']
        test_plan = self.u2000_test_results['test_plan']
        config_name = self.u2000_test_results['config_name']
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        start_tse = int(self.u2000_test_results['Start_TSE'])
        self.post_creation_data(i_settings, test_results, start_tse, parent, config_name, active_testplan_name, test_plan)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
        


       
            

        



   




