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
# import urllib3 
# from urllib3.poolmanager import PoolManager
from requests_toolbelt.multipart.encoder import MultipartEncoder

class agilentu2000:
    """Send script config to server.
    """
    global COMPANYNAME
    global HARDWARENAME
    global GAE_INSTANCE
    global USERNAME
    COMPANYNAME = 'Acme'
    HARDWARENAME = 'Tahoe'
    GAE_INSTANCE = 'gradientone-test'
    USERNAME = 'nedwards'

    def dt2ms(self, t):
        return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

    def __init__(self, u2000_test_results, s):
        self.u2000_test_results = u2000_test_results
        self.s = s

    def post_creation_data(self, i_settings, stuffing, start_tse, parent, config_name, active_testplan_name, test_plan) :
        s = self.s
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if test_plan == True:
            raw_data_url = "https://" + GAE_INSTANCE + ".appspot.com/u2000data/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
            url_t = "https://" + GAE_INSTANCE + ".appspot.com/u2000_testresults/" + COMPANYNAME + '/' + active_testplan_name + '/' + config_name
            window_u2000 = {'i_settings':i_settings, 'cha':stuffing, 'raw_data_url':raw_data_url, 'start_tse':start_tse, 'test_plan':test_plan, 'config_name':config_name, 'testplan_name':active_testplan_name, 'hardware_name':HARDWARENAME}
            out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
            r = s.post(url_t, data=out_u2000, headers=headers)
            #print "dir(r)=",dir(r)
            print "r.reason=",r.reason
            print "r.status_code=",r.status_code    
        else:
            raw_data_url = "https://" + GAE_INSTANCE + ".appspot.com/u2000data/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
            url_t = "https://" + GAE_INSTANCE + ".appspot.com/u2000_traceresults/" + COMPANYNAME + '/' + HARDWARENAME + '/' + config_name
            window_u2000 = {'i_settings':i_settings, 'cha':stuffing, 'raw_data_url':raw_data_url, 'start_tse':start_tse, 'test_plan':test_plan, 'config_name':config_name, 'testplan_name':active_testplan_name, 'hardware_name':HARDWARENAME}
            out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
            r = s.post(url_t, data=out_u2000, headers=headers)
            #print "dir(r)=",dir(r)
            print "r.reason=",r.reason
            print "r.status_code=",r.status_code

    def post_complete(self, active_testplan_name, config_name, test_plan, stop_tse, i_settings, start_tse, test_results):
        s = self.s
        window_complete = {'active_testplan_name':active_testplan_name, 'cha':test_results, 'config_name':config_name,'test_plan':test_plan, 'stop_tse':stop_tse, 'i_settings':i_settings, 'start_tse':start_tse, 'hardware_name':HARDWARENAME}
        out_complete = json.dumps(window_complete, ensure_ascii=True)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_c = "https://" + GAE_INSTANCE +".appspot.com/u2000_testcomplete/" + COMPANYNAME + '/' + active_testplan_name + '/' +config_name + "/%s" % str(stop_tse)
        c = s.post(url_c, data=out_complete, headers=headers)
        print "c.reason=",c.reason
        print "c.status_code=",c.status_code
        #print "dir(c)=",dir(c)

    def transmitraw(self):
        parent = 'raw'
        test_results = self.u2000_test_results['data']
        i_settings = self.u2000_test_results['i_settings']
        test_plan = self.u2000_test_results['test_plan']
        config_name = self.u2000_test_results['config_name']
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        start_tse = int(self.u2000_test_results['Start_TSE'])
        self.post_creation_data(i_settings, test_results, start_tse, parent, config_name, active_testplan_name, test_plan)

    def testcomplete(self):
        
        stop_tse = self.dt2ms(datetime.datetime.now())
        print self.u2000_test_results
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        config_name = self.u2000_test_results['config_name']
        test_plan = self.u2000_test_results['test_plan']
        i_settings = self.u2000_test_results['i_settings']
        start_tse = int(self.u2000_test_results['Start_TSE'])
        test_results = self.u2000_test_results['data']
        self.post_complete(active_testplan_name, config_name, test_plan, stop_tse, i_settings, start_tse, test_results)

    def transmitblob(self):
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        config_name = self.u2000_test_results['config_name']
        blob_u2000_test_results = self.u2000_test_results
        blob_u2000_test_results['max_value'] = blob_u2000_test_results['i_settings']['max_value']
        blob_u2000_test_results['min_value'] = blob_u2000_test_results['i_settings']['min_value']
        blob_u2000_test_results['pass_fail'] = blob_u2000_test_results['i_settings']['pass_fail']
        blob_u2000_test_results['pass_fail_type'] = blob_u2000_test_results['i_settings']['pass_fail_type']
        blob_u2000_test_results['correction_frequency'] = blob_u2000_test_results['i_settings']['correction_frequency']
        del blob_u2000_test_results['i_settings']
        filename = config_name + ':' + active_testplan_name 
        #f = open('/home/' + USERNAME + '/' + COMPANYNAME + '/Blobs/tempfile.csv', 'w')
        f = open('/home/nedwards/BitScope/Examples/tempfile.csv', 'w')
        w = csv.writer(f)
        w.writerow(blob_u2000_test_results.keys())
        w.writerow(blob_u2000_test_results.values())
        f.close()

        # m = MultipartEncoder(
        #           fields={'field0':(filename, open('/home/' + USERNAME + '/' + COMPANYNAME + '/Blobs/tempfile.csv', 'rb'), 'text/plain')}
        #           )
        m = MultipartEncoder(
                  fields={'field0':(filename, open('/home/nedwards/BitScope/Examples/tempfile.csv', 'rb'), 'text/plain')}
                  )
        blob_url = requests.get("https://"+ GAE_INSTANCE + ".appspot.com/upload/geturl")
        #m = MultipartEncoder(
        #        fields={'field0': ('tek0012ALL', open('../../DataFiles/tekcsv/tek0012ALL.csv', 'rb'), 'text/plain')}
        #        )
        b = requests.post(blob_url.text, data = m, headers={'Content-Type': m.content_type})
        print blob_url.text
        print "b.reason=",b.reason
        print "b.status_code=",b.status_code

if __name__ == "__main__":
    import doctest
    doctest.testmod()
        


       
            

        



   




