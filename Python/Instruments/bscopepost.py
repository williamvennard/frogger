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

    def roundup(self, x):
        return int(((x//100) * 100) + 10)

    def slicename_creation(self, x):

        slicename = x//100*100
        return slicename

    def post_creation(self, config_data, slicename, stuffing, start_tse, parent):
        window = {'config':config_data,'slicename':slicename,'data':stuffing, 'start_tse':start_tse}
        out = json.dumps(window)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if parent == 'raw':    
            #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
            url = "https://gradientone-test.appspot.com/bscopedata/arduino/%s" % slicename
        else:
            #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
            url = "https://gradientone-test.appspot.com/dec/bscopedata/arduino/%s" % slicename
        r = requests.post(url, data=out, headers=headers)
        #print "dir(r)=",dir(r)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code


    def end_creation(self, new_dtms):
        end = int(self.roundup(new_dtms))
        return end


    def transmitdec(self):
        parent = 'dec'
        test_results = self.bscope_test_results['data']
        config_data = self.bscope_test_results['Config']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        slicename = start_tse
        new_results = test_results[:1000]
        results_arr = np.array(new_results)  #puts the test data in an array
        dec = scipy.signal.decimate(results_arr, 10, ftype='fir', axis = 0)  #performs the decimation function
        test_results = dec.tolist()
        self.post_creation(config_data, slicename, test_results, start_tse, parent)

    def transmitraw(self):
        parent = 'raw'
        test_results = self.bscope_test_results['data']
        config_data = self.bscope_test_results['Config']
        start_tse = int(self.bscope_test_results['Start_TSE'])
        data_length = len(test_results)
        tse = start_tse
        stuffing = []
        for i in range(0, data_length, 10):
            chunk = str(test_results[i:i + 10])
            slicename = tse + i
            stuffing = chunk
            self.post_creation(config_data, slicename, stuffing, start_tse, parent)


            
if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




