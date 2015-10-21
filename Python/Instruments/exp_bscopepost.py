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

    def __init__(self, bscope_test_results, s):
        self.bscope_test_results = bscope_test_results
        self.active_testplan_name = bscope_test_results['active_testplan_name']
        self.config_name = bscope_test_results['config_name']
        self.test_plan = bscope_test_results['test_plan']
        self.s = s
        self.dec_factor = 10.0

    def dt2ms(self, t):
        return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)
 
    def get_payload(self, URL, payload_dict):
        return payload_dict[URL]

    def post_creation_data(self, i_settings, p_settings, stuffing, start_tse, parent, config_name, active_testplan_name, test_plan) :
        s = self.s
        window_bscope = {'i_settings':i_settings, 'p_settings':p_settings, 'cha':stuffing, 'start_tse':start_tse, 'test_plan':test_plan, 'testplan_name':active_testplan_name}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if test_plan == True:
            if parent == 'raw':    
                #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
                url_b = "https://gradientone-test.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
                out_bscope = json.dumps(window_bscope, ensure_ascii=True)
                r = s.post(url_b, data=out_bscope, headers=headers)
                #print "dir(r)=",dir(r)
                print "r.reason=",r.reason
                print "r.status_code=",r.status_code
            else:
                #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
                status = {'status':'Transmitting'}
                url_b = "https://gradientone-test.appspot.com/bscopedata/dec/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
                url_t = "https://gradientone-test.appspot.com/testresults/" + COMPANYNAME + '/' + active_testplan_name + '/' + config_name
                #url_s = "https://gradientone-test.appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
                #URL_list = [url_b, url_t, url_s]
                raw_url = "https://gradientone-test.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
                dec_url = "https://gradientone-test.appspot.com/bscopedata/dec/" + COMPANYNAME + '/'+ HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
                window_bscope = {'cha':stuffing}
                test_controls = {'p_settings':p_settings,'dec_data_url':dec_url,'test_plan':test_plan, 'raw_data_url':raw_url, 'start_tse':start_tse, 'config_name':config_name, 'hardware_name':HARDWARENAME, 'window_bscope':window_bscope}
                test_controls = json.dumps(test_controls, ensure_ascii=True)
                r = s.post(url_t, data=test_controls, headers=headers)
                #window_testresults = {'p_settings':p_settings,'dec_data_url':dec_url,'test_plan':test_plan, 'raw_data_url':raw_url, 'start_tse':start_tse, 'config_name':config_name, 'hardware_name':HARDWARENAME}
                #window_bscope = {'i_settings':i_settings, 'p_settings':p_settings, 'cha':stuffing, 'start_tse':start_tse}
                #payload_dict = {url_b:window_bscope, url_t:window_testresults, url_s:status}
                #rs = (grequests.post(u, session = s, json=self.get_payload(u, payload_dict), headers=headers) for u in URL_list)
                #grequests.map(rs)
        else:        
            if parent == 'raw':    
                #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
                url_b = "https://gradientone-test.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
                out_bscope = json.dumps(window_bscope, ensure_ascii=True)
                r = s.post(url_b, data=out_bscope, headers=headers)
                #print "dir(r)=",dir(r)
                print "r.reason=",r.reason
                print "r.status_code=",r.status_code
            else:
                #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
                status = {'status':'Transmitting'}
                url_b = "https://gradientone-test.appspot.com/bscopedata/dec/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % start_tse
                url_t = "https://gradientone-test.appspot.com/traceresults/" + COMPANYNAME + '/' + HARDWARENAME + '/' + config_name
                #url_s = "https://gradientone-test.appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
                #URL_list = [url_b, url_t, url_s]
                raw_url = "https://gradientone-test.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
                dec_url = "https://gradientone-test.appspot.com/bscopedata/dec/" + COMPANYNAME + '/'+ HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
                window_bscope = {'cha':stuffing}
                test_controls = {'i_settings':i_settings, 'p_settings':p_settings,'dec_data_url':dec_url,'test_plan':test_plan, 'raw_data_url':raw_url, 'start_tse':start_tse, 'config_name':config_name, 'hardware_name':HARDWARENAME, 'window_bscope':window_bscope}
                test_controls = json.dumps(test_controls, ensure_ascii=True)
                r = s.post(url_t, data=test_controls, headers=headers)
                #payload_dict = {url_b:window_bscope, url_t:window_testresults, url_s:status}
                #rs = (grequests.post(u, session = s, json=self.get_payload(u, payload_dict), headers=headers) for u in URL_list)
                #grequests.map(rs) 
    
    def post_complete(self, active_testplan_name, config_name, test_plan, stop_tse, i_settings, p_settings, start_tse,):
        s = self.s
        raw_url = "https://gradientone-test.appspot.com/bscopedata/" + COMPANYNAME + '/' + HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
        dec_url = "https://gradientone-test.appspot.com/bscopedata/dec/" + COMPANYNAME + '/'+ HARDWARENAME +'/' + config_name + "/%s" % str(start_tse)
        window_complete = {'active_testplan_name':active_testplan_name, 'dec_data_url':dec_url, 'raw_data_url':raw_url, 'config_name':config_name,'test_plan':test_plan, 'stop_tse':stop_tse, 'i_settings':i_settings, 'p_settings':p_settings, 'start_tse':start_tse, 'hardware_name':HARDWARENAME}
        out_complete = json.dumps(window_complete, ensure_ascii=True)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_c = "https://gradientone-test.appspot.com/testcomplete/" + COMPANYNAME + '/' + active_testplan_name + '/' +config_name + "/%s" % str(stop_tse)
        c = s.post(url_c, data=out_complete, headers=headers)
        print "c.reason=",c.reason
        print "c.status_code=",c.status_code
        #print "dir(c)=",dir(c)

    def transmitdec(self):
        parent = 'dec'
        dec_factor = self.dec_factor
        test_results = self.bscope_test_results['data']
        config_name = self.config_name
        active_testplan_name = self.active_testplan_name
        p_settings = self.bscope_test_results['p_settings']
        raw_msec_btw_samples = int(p_settings['Raw_msec_btw_samples'])
        p_settings['Dec_msec_btw_samples'] = 10 * raw_msec_btw_samples
        i_settings = self.bscope_test_results['i_settings']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        slicename = start_tse
        test_plan = self.test_plan
        print test_plan
        new_results = test_results[:6001]
        results_arr = np.array(new_results)  #puts the test data in an array
        dec = scipy.signal.decimate(results_arr, 5, ftype='fir', axis = 0)  #performs the decimation function
        test_results = dec.tolist()
        self.post_creation_data(i_settings, p_settings, test_results, start_tse, parent, config_name, active_testplan_name, test_plan)

    def transmitraw(self):
        parent = 'raw'
        dec_factor = self.dec_factor
        test_results = self.bscope_test_results['data']
        print test_results
        i_settings = self.bscope_test_results['i_settings']
        p_settings = self.bscope_test_results['p_settings']
        raw_msec_btw_samples = int(p_settings['Raw_msec_btw_samples'])
        p_settings['Dec_msec_btw_samples'] = 10 * raw_msec_btw_samples
        test_plan = self.test_plan
        config_name = self.config_name
        active_testplan_name = self.active_testplan_name
        start_tse = int(self.bscope_test_results['Start_TSE'])
        self.post_creation_data(i_settings, p_settings, test_results, start_tse, parent, config_name, active_testplan_name, test_plan)

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
        active_testplan_name = self.active_testplan_name
        config_name = self.config_name
        print config_name
        test_plan = self.test_plan
        p_settings = self.bscope_test_results['p_settings']
        p_settings['Dec_msec_btw_samples'] = 10
        i_settings = self.bscope_test_results['i_settings']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        self.post_complete(active_testplan_name, config_name, test_plan, stop_tse, i_settings, p_settings, start_tse)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




