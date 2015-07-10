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
#import urllib3 
#from urllib3.poolmanager import PoolManager
from requests_toolbelt.multipart.encoder import MultipartEncoder

class BitScope:
    """Parse BitScope output dictionary.

    Returns a class that can parse a bitscope output dictionary 
    and POST to the server.  The transmitdec class POSTs the 
    decimated data.  The transmitraw class POSTs the raw data.

    """


    def __init__(self, bscope_test_results):
        self.bscope_test_results = bscope_test_results


    def dt2ms(self, t):
        return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)


    def post_creation_data(self, i_settings, p_settings, slicename, stuffing, start_tse, parent):
        window_bscope = {'i_settings':i_settings, 'p_settings':p_settings,'slicename':slicename,'cha':stuffing, 'start_tse':start_tse}
        out_bscope = json.dumps(window_bscope)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if parent == 'raw':    
            #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
            url_b = "https://gradientone-test.appspot.com/bscopedata/LED/%s" % slicename
        else:
            #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
            url_b = "https://gradientone-test.appspot.com/bscopedata/dec/LED/%s" % slicename
        r = requests.post(url_b, data=out_bscope, headers=headers)
        #print "dir(r)=",dir(r)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code

    def post_creation_test(self, i_settings, p_settings, stuffing, start_tse):
        dec_url = 'https://gradientone-test.appspot.com/bscopedata/dec/LED/' + str(start_tse)
        raw_url = 'https://gradientone-test.appspot.com/bscopedata/LED/' + str(start_tse)
        window_testresults = {'p_settings':p_settings,'dec_data_url':dec_url, 'raw_data_url':raw_url, 'start_tse':start_tse}
        out_testresults = json.dumps(window_testresults)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_t = "https://gradientone-test.appspot.com/testresults/manufacturing/%s" % start_tse
        r = requests.post(url_t, data=out_testresults, headers=headers)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code
        #print "dir(r)=",dir(r)
    
    def post_complete(self, testplan_name, stop_tse):
        window_complete = {'testplan_name':testplan_name, 'stop_tse':stop_tse}
        out_complete = json.dumps(window_complete)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_c = "https://gradientone-test.appspot.com/testcomplete/research/%s" % stop_tse
        r = requests.post(url_c, data=out_complete, headers=headers)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code
        #print "dir(r)=",dir(r)

    def transmitdec(self):
        parent = 'dec'
        test_results = self.bscope_test_results['data']
        p_settings = self.bscope_test_results['p_settings']
        p_settings['Dec_msec_btw_samples'] = 10
        i_settings = self.bscope_test_results['i_settings']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        slicename = start_tse
        new_results = test_results[:1000]
        results_arr = np.array(new_results)  #puts the test data in an array
        dec = scipy.signal.decimate(results_arr, 10, ftype='fir', axis = 0)  #performs the decimation function
        test_results = dec.tolist()
        self.post_creation_data(i_settings, p_settings, slicename, test_results, start_tse, parent)

    def transmitraw(self):
        parent = 'raw'
        test_results = self.bscope_test_results['data']
        i_settings = self.bscope_test_results['i_settings']
        p_settings = self.bscope_test_results['p_settings']
        p_settings['Dec_msec_btw_samples'] = 10
        start_tse = int(self.bscope_test_results['Start_TSE'])
        slice_size = int(p_settings['Slice_Size_msec'])
        sample_rate = int(i_settings['Sample_Rate_Hz'])
        data_length = len(test_results)
        sample_per_slice = int((float(sample_rate)/1000)*float(slice_size))
        tse = start_tse
        stuffing = []
        self.post_creation_test(i_settings, p_settings, stuffing, start_tse)
        for i in range(0, data_length, sample_per_slice):
            chunk = str(test_results[i:i + sample_per_slice])
            slicename = tse + i
            stuffing = chunk
            self.post_creation_data(i_settings, p_settings, slicename, stuffing, start_tse, parent)

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
        testplan_name='manufacturing'
        self.post_complete(testplan_name, stop_tse)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




