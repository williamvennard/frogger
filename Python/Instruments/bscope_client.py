import json
import requests
import time   # time is a module here
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
MY_RATE = 1000 # default sample rate we'll use for capture. (hertz)
MY_SIZE = 500 # number of samples we'll capture (simply a connectivity test)
TRUE = 1
MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM")
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND")
sample_interval = 1 # (1 msec)


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
    return int(((x//10) * 10) + 10)

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


def bscope_acq(config):    
    """sets the configuration for the bitscope API and calls the BitScope class"""
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    if BL_Open(MY_PROBE_FILE,1):
        config_vars = check_config_vars(config)
        MY_RATE = float(config_vars[0])
        MY_SIZE = int(config_vars[1])
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
        config_dict = {'bitscope':'info'}
        config_dict = set_v_for_k(config_dict, 'Link', BL_Name(0))
        config_dict = set_v_for_k(config_dict, 'BitScope', (BL_Version(BL_VERSION_DEVICE), BL_ID()))
        config_dict = set_v_for_k(config_dict, 'Channels', (BL_Count(BL_COUNT_ANALOG) + BL_Count(BL_COUNT_LOGIC), 
                                                           BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC)))
        config_dict = set_v_for_k(config_dict, 'Library', (BL_Version(BL_VERSION_LIBRARY), BL_Version(BL_VERSION_BINDING))) 
        acq_dict = set_v_for_k(acq_dict, 'data', DATA) 
        acq_dict = set_v_for_k(acq_dict, 'Config', config_dict)    
        acq_dict = set_v_for_k(acq_dict, 'Start_TSE', roundup(tse))
        BL_Close()
        print "Finished: Library closed, resources released."    
        bits = BitScope(acq_dict)
        bits.transmitdec()
        bits.transmitraw()
    else:
        print "  FAILED: device not found (check your probe file)."
    
check_config_url()
