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

class BitScope:
    """Parse BitScope output dictionary.

    Returns a class that can parse a bitscope output dictionary 
    and POST to the server via the transmit method.

    """


    def __init__(self, bscope_test_results):
        self.bscope_test_results = bscope_test_results


    def dt2ms(self, t):
        return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

    def roundup(self, x):
        return int(((x//100) * 100) + 100)

    def slicename_creation(self, x):

        slicename = x//100*100
        return slicename

    def post_creation(self, slicename, stuffing):
        window = {'config':{'TEK':'TODO'},'slicename':slicename,'data':stuffing}
        out = json.dumps(window)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = "https://gradientone-dev1.appspot.com/bscopedata/arduino/%s" % slicename
        r = requests.post(url, data=out, headers=headers)
        print "dir(r)=",dir(r)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code


    def end_creation(self, new_dtms):
        end = int(self.roundup(new_dtms))
        return end

    def transmit(self):
        
        test_results = self.bscope_test_results['data']
        print test_results
        data_length = len(test_results)
        tse = test_results[0]['DTE']
        new_dtms = tse
        stuffing = []
        for i in range(0, data_length, 10):
            chunk = test_results[i:i + 10]
            end = self.end_creation(new_dtms)
            slicename = self.slicename_creation(new_dtms)
            for tr in chunk:
                new_dtms =  tr['DTE']
                if float(tr['DTE']) >= end:
                    self.post_creation(slicename, stuffing)
                    stuffing = []
                    slicename = self.slicename_creation(new_dtms)  
                    stuffing.append(tr)
                    end = self.end_creation(new_dtms)
                    continue
                stuffing.append(tr)
            slicename = self.slicename_creation(new_dtms)
            self.post_creation(slicename, stuffing)
            stuffing = []
        

            
if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




