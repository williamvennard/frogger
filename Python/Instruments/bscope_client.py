import json
import requests
import time
import datetime
import threading
from bitlib import *
from bscopepost import BitScope
import numpy
import scipy.signal 


#Default settings.  MY_RATE & MY_SIZE are configurable.  This may change.
MY_DEVICE = 0 # one open device only
MY_CHANNEL = 0 # channel to capture and display
MY_PROBE_FILE = "" # default probe file if unspecified 
MY_MODE = BL_MODE_FAST # preferred capture mode
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


def check_config_vars(config):
    if config[0]['number_of_samples'] != 'None':
        MY_SIZE = config[0]['number_of_samples']
    if config[0]['sample_rate'] != 'None':
        MY_RATE = config[0]['sample_rate']
    return MY_RATE, MY_SIZE

def set_v_for_k(test_dict, k, v):
    test_dict[k] = v
    return test_dict

def roundup(x):
    return int(((x//100) * 100) + 100)

def make_json(payload):
    acq_dict = json.dumps(payload)
    return acq_dict

def check_config_url():
    """polls the configuration URL for a start signal @ 1sec intervals"""
    r = requests.get('http://gradientone-dev1.appspot.com/configoutput/nedwards/Bscope/LEDTESTER2')
    config = r.json()
    if check_start(config) == 'True':
	    print "Starting API"
	    bscope_acq(config)
    else:
        print "No start order found"
    threading.Timer(1, check_config_url()).start()

def make_data_dict(DATA, tse, time):
    """ creates the dictionary of data from the bitscope"""
    new_data = []
    tse = roundup(tse)
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
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    if BL_Open(MY_PROBE_FILE,1):
        config_vars = check_config_vars(config)
        MY_RATE = config_vars[0]
        MY_SIZE = config_vars[1]
        BL_Select(BL_SELECT_DEVICE,MY_DEVICE)
        BL_Mode(BL_MODE_LOGIC) == BL_MODE_LOGIC or BL_Mode(BL_MODE_FAST)
        BL_Range(BL_Count(BL_COUNT_RANGE))
        BL_Mode(MY_MODE) # prefered capture mode
        BL_Intro(BL_ZERO); # optional, default BL_ZERO
        BL_Delay(BL_ZERO); # optional, default BL_ZERO
        BL_Rate(MY_RATE); # optional, default BL_MAX_RATE
        BL_Size(MY_SIZE); # optional default BL_MAX_SIZE
        BL_Select(BL_SELECT_CHANNEL,MY_CHANNEL); # choose the channel
        BL_Trigger(BL_ZERO,BL_TRIG_RISE); # optional when untriggered */
        BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD); # use the POD input */
        BL_Range(BL_Count(BL_COUNT_RANGE)); # maximum range
        BL_Offset(BL_ZERO); # optional, default 0
        BL_Enable(TRUE); # at least one channel must be initialised 
        BL_Trace()
        tse = dt2ms(datetime.datetime.now())
        DATA = BL_Acquire()
        new_data = make_data_dict(DATA, tse, time)
        config_dict = {}
        config_dict = set_v_for_k(config_dict, 'Link', BL_Name(0))
        config_dict = set_v_for_k(config_dict, 'BitScope', (BL_Version(BL_VERSION_DEVICE), BL_ID()))
        config_dict = set_v_for_k(config_dict, 'Channels', (BL_Count(BL_COUNT_ANALOG) + BL_Count(BL_COUNT_LOGIC), 
                                                           BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC)))
        config_dict = set_v_for_k(config_dict, 'Library', (BL_Version(BL_VERSION_LIBRARY), BL_Version(BL_VERSION_BINDING))) 
        acq_dict = set_v_for_k(acq_dict, 'data', new_data) 
        acq_dict = set_v_for_k(acq_dict, 'Config', config_dict)    
        BL_Close()
        print "Finished: Library closed, resources released."    
        #print acq_dict
        bits = BitScope(acq_dict)
        bits.transmitdec()
        bits.transmitraw()
    else:
        print "  FAILED: device not found (check your probe file)."
    
check_config_url()
