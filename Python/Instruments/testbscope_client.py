import json
import requests
import time
import datetime
import threading
#from bitlib import *
from testbscopepost import BitScope
import numpy
import scipy.signal 


MY_DEVICE = 0 # one open device only
MY_CHANNEL = 0 # channel to capture and display
MY_PROBE_FILE = "" # default probe file if unspecified 
#MY_MODE = BL_MODE_FAST # preferred capture mode
MY_RATE = 1000000 # default sample rate we'll use for capture.
MY_SIZE = 500 # number of samples we'll capture (simply a connectivity test)
TRUE = 1
MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM")
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND")
sample_interval = 10
time = 0.00

def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def check_start(config):
    start_measurement = str(config[0]['start_measurement'])
    return start_measurement

def set_v_for_k(test_dict, k, v):
    test_dict[k] = v
    return test_dict

def make_json(payload):
    acq_dict = json.dumps(payload)
    return acq_dict

def check_config_url():
    """polls the configuration URL for a start signal @ 1sec intervals"""
    r = requests.get('http://gradientone-dev1.appspot.com/configoutput/nedwards/Bscope/LEDTESTER2')
    config = r.json()
    if check_start(config) == 'True':
        check_config_vars(config)
        print "Starting API"
        bscope_acq(config)
    else:
        print "No start order found"
    threading.Timer(60, check_config_url()).start()

def check_config_vars(config):
    if config[0]['number_of_samples'] == 'None':
        pass
    if config[0]['sample_rate'] == 'None':
        pass
    return MY_RATE, MY_SIZE


def make_data_dict(DATA, tse, time):
    """ creates the dictionary of data from the bitscope"""
    new_data = []
    for datum in DATA:
        temp_dict = {}
        temp_dict = set_v_for_k(temp_dict, 'CHA', datum)
        temp_dict = set_v_for_k(temp_dict, 'DTE', tse)
        temp_dict = set_v_for_k(temp_dict, 'TIME', time)
        tse = tse + sample_interval
        time = round((time + 0.01),2)
        new_data.append(temp_dict)
    return new_data


def bscope_acq(config):    
    """sets the configuration for the bitscope API and calls the BitScope class"""

    config_vars = check_config_vars(config)
    print config_vars
    MY_RATE = config_vars[0]
    MY_SIZE = config_vars[1]
    print MY_RATE
    print MY_SIZE
    acq_dict = {'Config': {'Channels': (10, 2, 8), 'BitScope': ('BS000501', 'KD58VM58'), 'Link': 'USB:/dev/ttyUSB0', 'Library': ('2.0 FE26A', 'Python DC01L')}, 
    'data': [{'CHA': 1.76171875, 'DTE': 1435416650934, 'TIME': 0.0}, {'CHA': 1.76171875, 'DTE': 1435416650944, 'TIME': 0.01}, 
    {'CHA': 1.76171875, 'DTE': 1435416650954, 'TIME': 0.02}, {'CHA': 1.76171875, 'DTE': 1435416650964, 'TIME': 0.03}, 
    {'CHA': 1.76171875, 'DTE': 1435416650974, 'TIME': 0.04}, {'CHA': 1.76171875, 'DTE': 1435416650984, 'TIME': 0.05}, 
    {'CHA': 1.76171875, 'DTE': 1435416650994, 'TIME': 0.06}, {'CHA': 1.76171875, 'DTE': 1435416651004, 
    'TIME': 0.07}, {'CHA': 1.76171875, 'DTE': 1435416651014, 'TIME': 0.08}, {'CHA': 1.76171875, 'DTE': 1435416651024, 'TIME': 0.09}]}
    bits = BitScope(acq_dict)
    #bits.transmitdec()
    bits.transmitraw()

    
check_config_url()
