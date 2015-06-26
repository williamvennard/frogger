"""
This is the "time_based_paging_bscope" script.

"""

import time
import datetime 
import math
import csv
import itertools
import json
import requests
from itertools import izip_longest
from itertools import izip

class BitScope:

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
        #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
        r = requests.post(url, data=out, headers=headers)
        print "dir(r)=",dir(r)
        print "r.reason=",r.reason
        print "r.status_code=",r.status_code

    #bscope_test_results = {'data': [{'CHA': -5.5, 'DTE': 1435283518693, 'TIME': 0.0}, {'CHA': -5.5, 'DTE': 1435283518703, 'TIME': 0.01}, {'CHA': -5.5, 'DTE': 1435283518713, 'TIME': 0.02}, {'CHA': -5.5, 'DTE': 1435283518723, 'TIME': 0.03}, {'CHA': -5.5, 'DTE': 1435283518733, 'TIME': 0.04}, {'CHA': -5.5, 'DTE': 1435283518743, 'TIME': 0.05}, {'CHA': -5.5, 'DTE': 1435283518753, 'TIME': 0.06}, {'CHA': -5.5, 'DTE': 1435283518763, 'TIME': 0.07}, {'CHA': -5.5, 'DTE': 1435283518773, 'TIME': 0.08}, {'CHA': -5.5, 'DTE': 1435283518783, 'TIME': 0.09}, {'CHA': -5.5, 'DTE': 1435283518793, 'TIME': 0.1}, {'CHA': -5.5, 'DTE': 1435283518803, 'TIME': 0.11}, {'CHA': -5.5, 'DTE': 1435283518813, 'TIME': 0.12}, {'CHA': -5.5, 'DTE': 1435283518823, 'TIME': 0.13}, {'CHA': -5.5, 'DTE': 1435283518833, 'TIME': 0.14}, {'CHA': -5.5, 'DTE': 1435283518843, 'TIME': 0.15}, {'CHA': -5.5, 'DTE': 1435283518853, 'TIME': 0.16}, {'CHA': -5.5, 'DTE': 1435283518863, 'TIME': 0.17}, {'CHA': -5.5, 'DTE': 1435283518873, 'TIME': 0.18}, {'CHA': -5.5, 'DTE': 1435283518883, 'TIME': 0.19}, {'CHA': -5.5, 'DTE': 1435283518893, 'TIME': 0.2}, {'CHA': -5.5, 'DTE': 1435283518903, 'TIME': 0.21}, {'CHA': -5.5, 'DTE': 1435283518913, 'TIME': 0.22}, {'CHA': -5.5, 'DTE': 1435283518923, 'TIME': 0.23}, {'CHA': -5.5, 'DTE': 1435283518933, 'TIME': 0.24}, {'CHA': -5.5, 'DTE': 1435283518943, 'TIME': 0.25}, {'CHA': -5.5, 'DTE': 1435283518953, 'TIME': 0.26}, {'CHA': -5.5, 'DTE': 1435283518963, 'TIME': 0.27}, {'CHA': -5.5, 'DTE': 1435283518973, 'TIME': 0.28}, {'CHA': -5.5, 'DTE': 1435283518983, 'TIME': 0.29}, {'CHA': -5.5, 'DTE': 1435283518993, 'TIME': 0.3}, {'CHA': -5.5, 'DTE': 1435283519003, 'TIME': 0.31}, {'CHA': -5.5, 'DTE': 1435283519013, 'TIME': 0.32}, {'CHA': -5.5, 'DTE': 1435283519023, 'TIME': 0.33}, {'CHA': -5.5, 'DTE': 1435283519033, 'TIME': 0.34}, {'CHA': -5.5, 'DTE': 1435283519043, 'TIME': 0.35}, {'CHA': -5.5, 'DTE': 1435283519053, 'TIME': 0.36}, {'CHA': -5.5, 'DTE': 1435283519063, 'TIME': 0.37}, {'CHA': -5.5, 'DTE': 1435283519073, 'TIME': 0.38}, {'CHA': -5.5, 'DTE': 1435283519083, 'TIME': 0.39}, {'CHA': -5.5, 'DTE': 1435283519093, 'TIME': 0.4}, {'CHA': -5.5, 'DTE': 1435283519103, 'TIME': 0.41}, {'CHA': -5.5, 'DTE': 1435283519113, 'TIME': 0.42}, {'CHA': -5.5, 'DTE': 1435283519123, 'TIME': 0.43}, {'CHA': -5.5, 'DTE': 1435283519133, 'TIME': 0.44}, {'CHA': -5.5, 'DTE': 1435283519143, 'TIME': 0.45}, {'CHA': -5.5, 'DTE': 1435283519153, 'TIME': 0.46}, {'CHA': -5.5, 'DTE': 1435283519163, 'TIME': 0.47}, {'CHA': -5.5, 'DTE': 1435283519173, 'TIME': 0.48}, {'CHA': -5.5, 'DTE': 1435283519183, 'TIME': 0.49}, {'CHA': -5.5, 'DTE': 1435283519193, 'TIME': 0.5}, {'CHA': -5.5, 'DTE': 1435283519203, 'TIME': 0.51}, {'CHA': -5.5, 'DTE': 1435283519213, 'TIME': 0.52}, {'CHA': -5.5, 'DTE': 1435283519223, 'TIME': 0.53}, {'CHA': -5.5, 'DTE': 1435283519233, 'TIME': 0.54}, {'CHA': -5.5, 'DTE': 1435283519243, 'TIME': 0.55}, {'CHA': -5.5, 'DTE': 1435283519253, 'TIME': 0.56}, {'CHA': -5.5, 'DTE': 1435283519263, 'TIME': 0.57}, {'CHA': -5.5, 'DTE': 1435283519273, 'TIME': 0.58}, {'CHA': -5.5, 'DTE': 1435283519283, 'TIME': 0.59}, {'CHA': -5.5, 'DTE': 1435283519293, 'TIME': 0.6}, {'CHA': -5.5, 'DTE': 1435283519303, 'TIME': 0.61}, {'CHA': -5.5, 'DTE': 1435283519313, 'TIME': 0.62}, {'CHA': -5.5, 'DTE': 1435283519323, 'TIME': 0.63}, {'CHA': -5.5, 'DTE': 1435283519333, 'TIME': 0.64}, {'CHA': -5.5, 'DTE': 1435283519343, 'TIME': 0.65}, {'CHA': -5.5, 'DTE': 1435283519353, 'TIME': 0.66}, {'CHA': -5.5, 'DTE': 1435283519363, 'TIME': 0.67}, {'CHA': -5.5, 'DTE': 1435283519373, 'TIME': 0.68}, {'CHA': -5.5, 'DTE': 1435283519383, 'TIME': 0.69}, {'CHA': -5.5, 'DTE': 1435283519393, 'TIME': 0.7}, {'CHA': -5.5, 'DTE': 1435283519403, 'TIME': 0.71}, {'CHA': -5.5, 'DTE': 1435283519413, 'TIME': 0.72}, {'CHA': -5.5, 'DTE': 1435283519423, 'TIME': 0.73}, {'CHA': -5.5, 'DTE': 1435283519433, 'TIME': 0.74}, {'CHA': -5.5, 'DTE': 1435283519443, 'TIME': 0.75}, {'CHA': -5.5, 'DTE': 1435283519453, 'TIME': 0.76}, {'CHA': -5.5, 'DTE': 1435283519463, 'TIME': 0.77}, {'CHA': -5.5, 'DTE': 1435283519473, 'TIME': 0.78}, {'CHA': -5.5, 'DTE': 1435283519483, 'TIME': 0.79}, {'CHA': -5.5, 'DTE': 1435283519493, 'TIME': 0.8}, {'CHA': -5.5, 'DTE': 1435283519503, 'TIME': 0.81}, {'CHA': -5.5, 'DTE': 1435283519513, 'TIME': 0.82}, {'CHA': -5.5, 'DTE': 1435283519523, 'TIME': 0.83}, {'CHA': -5.5, 'DTE': 1435283519533, 'TIME': 0.84}, {'CHA': -5.5, 'DTE': 1435283519543, 'TIME': 0.85}, {'CHA': -5.5, 'DTE': 1435283519553, 'TIME': 0.86}, {'CHA': -5.5, 'DTE': 1435283519563, 'TIME': 0.87}, {'CHA': -5.5, 'DTE': 1435283519573, 'TIME': 0.88}, {'CHA': -5.5, 'DTE': 1435283519583, 'TIME': 0.89}, {'CHA': -5.5, 'DTE': 1435283519593, 'TIME': 0.9}, {'CHA': -5.5, 'DTE': 1435283519603, 'TIME': 0.91}, {'CHA': -5.5, 'DTE': 1435283519613, 'TIME': 0.92}, {'CHA': -5.5, 'DTE': 1435283519623, 'TIME': 0.93}, {'CHA': -5.5, 'DTE': 1435283519633, 'TIME': 0.94}, {'CHA': -5.5, 'DTE': 1435283519643, 'TIME': 0.95}, {'CHA': -5.5, 'DTE': 1435283519653, 'TIME': 0.96}, {'CHA': -5.5, 'DTE': 1435283519663, 'TIME': 0.97}, {'CHA': -5.5, 'DTE': 1435283519673, 'TIME': 0.98}, {'CHA': -5.5, 'DTE': 1435283519683, 'TIME': 0.99}], 'Config': {'Channels': (10, 2, 8), 'BitScope': ('BS001003', 'SIMULATE'), 'Link': 'NIL:BS001003:SIMULATE:METACHIP'}, 'Library': ('2.0 FE26A', 'Python DC01L')}


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
        

            


        


       
            

        



   




