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
import numpy as np
import scipy.signal 
import os, sys, stat
import csv
import grequests
#import urllib3 
#from urllib3.poolmanager import PoolManager
#from requests_toolbelt.multipart.encoder import MultipartEncoder

class BitScope:
    """Parse BitScope output dictionary.

    Returns a class that can parse a bitscope output dictionary 
    and POST to the server.  The transmitdec class POSTs the 
    decimated data.  The transmitraw class POSTs the raw data.

    """
    global COMPANYNAME
    global HARDWARENAME
    COMPANYNAME = 'Acme'
    HARDWARENAME = 'Tahoe'

    def __init__(self, bscope_test_results):
        self.bscope_test_results = bscope_test_results
        self.testplan_name = bscope_test_results['testplan_name']
        self.instrument_name = bscope_test_results['instrument_name']
        self.test_plan = bscope_test_results['test_plan']

    def dt2ms(self, t):
        return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)
 
    def get_payload(self, URL, payload_dict):
        return payload_dict[URL]

    def post_creation_data(self, i_settings, p_settings, stuffing, start_tse, parent, instrument_name, testplan_name, test_plan) :
        window_bscope = {'i_settings':i_settings, 'p_settings':p_settings, 'cha':stuffing, 'start_tse':start_tse}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if parent == 'raw':    
            #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
            url_b = "https://gradientone-dev1.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + instrument_name + "/%s" % start_tse
            out_bscope = json.dumps(window_bscope, ensure_ascii=True)
            r = requests.post(url_b, data=out_bscope, headers=headers)
            #print "dir(r)=",dir(r)
            print "r.reason=",r.reason
            print "r.status_code=",r.status_code
        else:
            #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
            url_b = "https://gradientone-dev1.appspot.com/bscopedata/dec/" + COMPANYNAME + '/' + HARDWARENAME +'/' + instrument_name + "/%s" % start_tse
            url_t = "https://gradientone-dev1.appspot.com/testresults/" + COMPANYNAME + '/' + testplan_name + "/%s" % str(start_tse)
            URL_list = [url_b, url_t]
            raw_url = "https://gradientone-dev1.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + instrument_name + "/%s" % str(start_tse)
            dec_url = "https://gradientone-dev1.appspot.com/bscopedata/dec/" + COMPANYNAME + '/'+ HARDWARENAME +'/' + instrument_name + "/%s" % str(start_tse)
            window_testresults = {'p_settings':p_settings,'dec_data_url':dec_url,'test_plan':test_plan, 'raw_data_url':raw_url, 'start_tse':start_tse, 'instrument_name':instrument_name, 'hardware_name':HARDWARENAME}
            window_bscope = {'i_settings':i_settings, 'p_settings':p_settings, 'cha':stuffing, 'start_tse':start_tse}
            payload_dict = {url_b:window_bscope, url_t:window_testresults}
            rs = (grequests.post(u, json=self.get_payload(u, payload_dict), headers=headers) for u in URL_list)
            grequests.map(rs)
    
    def post_complete(self, testplan_name, instrument_name, test_plan, stop_tse, i_settings, p_settings, start_tse,):
        raw_url = "https://gradientone-dev1.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + instrument_name + "/%s" % str(start_tse)
        dec_url = "https://gradientone-dev1.appspot.com/bscopedata/dec/" + COMPANYNAME + '/'+ HARDWARENAME +'/' + instrument_name + "/%s" % str(start_tse)
        window_complete = {'testplan_name':testplan_name, 'dec_data_url':dec_url, 'raw_data_url':raw_url, 'instrument_name':instrument_name,'test_plan':test_plan, 'stop_tse':stop_tse, 'i_settings':i_settings, 'p_settings':p_settings, 'start_tse':start_tse, 'hardware_name':HARDWARENAME}
        out_complete = json.dumps(window_complete, ensure_ascii=True)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_c = "https://gradientone-dev1.appspot.com/testcomplete/" + COMPANYNAME + '/' + testplan_name + "/%s" % str(stop_tse)
        c = requests.post(url_c, data=out_complete, headers=headers)
        print "c.reason=",c.reason
        print "c.status_code=",c.status_code
        #print "dir(c)=",dir(c)

    def transmitdec(self):
        parent = 'dec'
        test_results = self.bscope_test_results['data']
        instrument_name = self.instrument_name
        testplan_name = self.testplan_name
        p_settings = self.bscope_test_results['p_settings']
        p_settings['Dec_msec_btw_samples'] = 10
        i_settings = self.bscope_test_results['i_settings']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        slicename = start_tse
        test_plan = self.test_plan
        new_results = test_results[:1000]
        results_arr = np.array(new_results)  #puts the test data in an array
        dec = scipy.signal.decimate(results_arr, 10, ftype='fir', axis = 0)  #performs the decimation function
        test_results = dec.tolist()
        self.post_creation_data(i_settings, p_settings, test_results, start_tse, parent, instrument_name, testplan_name, test_plan)

    def transmitraw(self):
        parent = 'raw'
        test_results = self.bscope_test_results['data']
        print test_results
        i_settings = self.bscope_test_results['i_settings']
        p_settings = self.bscope_test_results['p_settings']
        test_plan = self.test_plan
        instrument_name = self.instrument_name
        testplan_name = self.testplan_name
        p_settings['Dec_msec_btw_samples'] = 10
        start_tse = int(self.bscope_test_results['Start_TSE'])
        self.post_creation_data(i_settings, p_settings, test_results, start_tse, parent, instrument_name, testplan_name, test_plan)

    def transmitblob(self):
        f = open('/home/nedwards/BitScope/Examples/tempfile.csv', 'w')
        w = csv.writer(f)
        w.writerow(self.bscope_test_results.keys())
        w.writerow(self.bscope_test_results.values())
        f.close()
        m = MultipartEncoder(
                  fields={'field0':('BitScope', open('/home/nedwards/BitScope/Examples/tempfile.csv', 'rb'), 'text/plain')}
                  )
        blob_url = requests.get("https://gradientone-test.appspot.com/upload/geturl")
        #m = MultipartEncoder(
        #        fields={'field0': ('tek0012ALL', open('../../DataFiles/tekcsv/tek0012ALL.csv', 'rb'), 'text/plain')}
        #        )
        b = requests.post(blob_url.text, data = m, headers={'Content-Type': m.content_type})
        print "b.reason=",b.reason
        print "b.status_code=",b.status_code

    def testcomplete(self):
        
        stop_tse = self.dt2ms(datetime.datetime.now())
        testplan_name = self.testplan_name
        instrument_name = self.instrument_name
        test_plan = self.test_plan
        p_settings = self.bscope_test_results['p_settings']
        p_settings['Dec_msec_btw_samples'] = 10
        i_settings = self.bscope_test_results['i_settings']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        self.post_complete(testplan_name, instrument_name, test_plan, stop_tse, i_settings, p_settings, start_tse)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




