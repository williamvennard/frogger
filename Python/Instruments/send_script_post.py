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

class Script:
    """Send script config to server.
    """
    global COMPANYNAME
    global HARDWARENAME
    COMPANYNAME = 'Acme'
    HARDWARENAME = 'Tahoe'

    def __init__(self, config,name):
        self.config = config
        self.name = name

    def transmit_config(self):
        config = self.config
        name = self.name
        print config
        config['name'] = name
        out = json.dumps(config)
        url = "http://localhost:18080/scriptconfig" 
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=out, headers=headers)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code
        #print "dir(r)=",dir(r)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

        


       
            

        



   




