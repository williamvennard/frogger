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
MY_RATE = 1000 # default sample rate we'll use for capture (hertz).  1 sample every 1 milisecond.
MY_SIZE = 5000 # number of samples we'll capture (simply a connectivity test)
SLICE_SIZE = 100 # miliseconds
TRUE = 1
MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM")
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND")
COMPANYNAME = 'Acme'
HARDWARENAME ='Tahoe'


def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def check_start(config):
    commence_test = str(config['commence_test'])
    return commence_test

def post_status(status):
    "posts hardware status updates to the server"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    status = json.dumps(status, ensure_ascii=True)
    url_s = "https://gradientone-dev1.appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
    s = requests.post(url_s, data=status, headers=headers)
    print "s.reason=",s.reason
    print "s.status_code=",s.status_code
    #print "dir(s)=",dir(s)

def check_config_vars(config):
    "creates config variables to pass to the main BitScope code"
    if config['test_plan'] == 'True':
        testplan_name = config['testplan_name']
        instrument_name = config['inst_config']['instrument_name']
        MY_RATE = config['inst_config']['sample_rate']
        MY_SIZE = config['inst_config']['number_of_samples']
        test_plan =config['test_plan']
    else:
        testplan_name = config['testplan_name']
        test_plan = 'False'
        instrument_name = config['instrument_name']
        MY_RATE = config['sample_rate']
        MY_SIZE = config['number_of_samples']
    return testplan_name, instrument_name, MY_RATE, MY_SIZE, test_plan

def set_v_for_k(test_dict, k, v):
    "creates dictionary based off empty dictionary and key/value args"
    test_dict[k.encode('ascii')] = v
    return test_dict

def roundup(x):
    return int(((x//SLICE_SIZE) * SLICE_SIZE) + SLICE_SIZE)

def make_json(payload):
    "makes json based off input payload"
    acq_dict = json.dumps(payload)
    return acq_dict

def check_config_url():
    """polls the configuration URL for a start signal @ 1sec intervals"""
    config_url = "https://gradientone-dev1.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    r = requests.get(config_url)
    if r:
        config = r.json()
        config = config['configs'][0]
        if check_start(config) == 'True':
            print "Starting API"
            post_status('Starting')
            bscope_acq(config)
        else:
            print "No start order found"
    threading.Timer(1, check_config_url()).start()

def bscope_acq(config):    
    """sets the configuration for the bitscope API and calls the BitScope class"""
    time_start = time.time()
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    post_status('Acquiring')
    if BL_Open(MY_PROBE_FILE,1):
        config_vars = check_config_vars(config)
        testplan_name = config_vars[0]
        instrument_name = config_vars[1]
        MY_RATE = float(config_vars[2])
        MY_SIZE = int(config_vars[3])
        test_plan = config_vars[4]
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
        SAMPLE_SIZE = len(DATA)
        MY_SAMPLE_INTERVAL = int(1/MY_RATE*1000) #interval between sample in msec
        Total_Slices = SAMPLE_SIZE/SLICE_SIZE
        config_dict = {}
        plot_dict = {}
        inst_dict ={}
        inst_dict = set_v_for_k(inst_dict, 'Link', BL_Name(0))
        inst_dict = set_v_for_k(inst_dict, 'BitScope', [BL_Version(BL_VERSION_DEVICE), BL_ID()])
        inst_dict = set_v_for_k(inst_dict, 'Channels', [BL_Count(BL_COUNT_ANALOG) + BL_Count(BL_COUNT_LOGIC), 
                                                           BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC)])
        inst_dict = set_v_for_k(inst_dict, 'Library', [BL_Version(BL_VERSION_LIBRARY), BL_Version(BL_VERSION_BINDING)]) 
        inst_dict = set_v_for_k(inst_dict, 'Sample_Rate_Hz', MY_RATE)
        inst_dict = set_v_for_k(inst_dict, 'Sample_Size', SAMPLE_SIZE)
        plot_dict = set_v_for_k(plot_dict, 'Total_Slices', Total_Slices)
        plot_dict = set_v_for_k(plot_dict, 'Slice_Size_msec', SLICE_SIZE)
        plot_dict = set_v_for_k(plot_dict, 'Raw_msec_btw_samples', MY_SAMPLE_INTERVAL)
        plot_dict = set_v_for_k(plot_dict, 'Start_TSE', str(roundup(tse)))
        config_dict = set_v_for_k(config_dict,'Plot_Settings', plot_dict)
        config_dict = set_v_for_k(config_dict,'Inst_Settings', inst_dict)
        acq_dict = set_v_for_k(acq_dict, 'data', DATA) 
        acq_dict = set_v_for_k(acq_dict, 'i_settings', inst_dict)    
        acq_dict = set_v_for_k(acq_dict, 'p_settings', plot_dict)
        acq_dict = set_v_for_k(acq_dict, 'testplan_name', testplan_name)
        acq_dict = set_v_for_k(acq_dict, 'instrument_name', instrument_name)
        acq_dict = set_v_for_k(acq_dict, 'test_plan', test_plan)
        acq_dict = set_v_for_k(acq_dict, 'Start_TSE', (roundup(tse)))
        BL_Close()
        time_bs = time.time()
        print "Finished: Library closed, resources released."    
        post_status('Transmitting')
        bits = BitScope(acq_dict)
        bits.transmitdec()
        time_dec = time.time()
        bits.transmitraw()
        time_stop = time.time()
        #bits.transmitblob()
        bits.testcomplete()
        post_status('Idle')
        bs_time = time_bs - time_start
        dec_time = time_dec - time_start
        raw_time = time_stop - time_dec
        total_time = time_stop - time_start
        print 'BS data acq time', bs_time
        #print 'time between data acq and transmit dec data', dec_time
        #print 'time after dec transmission and transmit raw data', raw_time
        print 'total time', total_time
    else:
        print "  FAILED: device not found (check your probe file)."

post_status('Idle')
check_config_url()
