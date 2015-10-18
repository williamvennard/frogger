import json
import requests
import grequests
import time   # time is a module here
import math
import datetime
import threading
from u2000_post import u2000
import numpy as np
import numpy.fft as fft
import scipy.signal 
import ivi



def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def post_status(status):
    "posts hardware status updates to the server"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    window = {'status':status, 'time':time.time()}
    status = json.dumps(window, ensure_ascii=True)
    url_s = "https://gradientone-test.appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
    s = requests.post(url_s, data=status, headers=headers)
    print "s.reason=",s.reason
    print "s.status_code=",s.status_code
    #print "dir(s)=",dir(s)

def check_config_vars(config):
    "creates config variables to pass to the main u2000 code"
    if config['test_plan'] == 'True':
        active_testplan_name = config['active_testplan_name']
        config_name = config['config_name']
        averaging_count_auto = config['averaging_count_auto']
        correction_frequency= config['correction_frequency']
        offset= config['offset']
        channel_name= config['channel_name']
        range_auto= config['range_auto']
        units= config['units']
        test_plan =config['test_plan']
    else:
        active_testplan_name = config['active_testplan_name']
        test_plan = 'False'
        config_name = config['config_name']
        averaging_count_auto = config['averaging_count_auto']
        correction_frequency= config['correction_frequency']
        offset= config['offset']
        channel_name= config['channel_name']
        range_auto= config['range_auto']
        units= config['units']
    return active_testplan_name, config_name, averaging_count_auto, correction_frequency, offset, channel_name, range_auto, units


def set_v_for_k(test_dict, k, v):
    "creates dictionary based off empty dictionary and key/value args"
    test_dict[k.encode('ascii')] = v
    return test_dict


def make_json(payload):
    "makes json based off input payload"
    acq_dict = json.dumps(payload)
    return acq_dict

def check_config_url():
    """polls the configuration URL for a start signal @ 1sec intervals"""
    config_url = "https://gradientone-test.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
   
    s = requests.session()
    r = s.get(config_url)
    if r:
        print 'checking'
        config = r.json()
        if config['configs_tps_traces']:
            config = config['configs_tps_traces'][0]
            if config['commence_test'] == 'True':  
                print "Starting API"
                post_status('Starting')
                u2000_acq(config, s)
        else:
            print "No start order found"
    threading.Timer(1, check_config_url()).start()


def u2000_acq(config, s):    
    """sets the configuration for the u2000 API and calls the u2000 class"""
    time_start = time.time()
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    config_vars = check_config_vars(config)
        return active_testplan_name, config_name, averaging_count_auto, correction_frequency, offset, channel_name, range_auto, units
    u2000 = ivi.agilent.u2000("USB0::2391::5973::MY********::INSTR")
    u2000.channels['channel1']
    # configure channel
    u2000.channels['channel1'].averaging_count_auto = config_vars[2]
    u2000.channels['channel1'].correction_frequency = config_vars[3]
    u2000.channels['channel1'].offset = config_vars[4]
    u2000.channels['channel1'].range_auto = config_vars[6]
    u2000.channels['channel1'].units = config_vars[7]
    #   initiate measurement
    u2000.measurement.initiate()
    # read out channel 1 power data
    post_status('Acquiring')
    power = u2000.channels['channel1'].measurement.fetch()
    tse = dt2ms(datetime.datetime.now())
    config_dict = {}
    plot_dict = {}
    inst_dict ={}
    inst_dict = set_v_for_k(inst_dict, 'averaging_count_auto', averaging_count_auto)
    inst_dict = set_v_for_k(inst_dict, 'correction_frequency', correction_frequency)
    inst_dict = set_v_for_k(inst_dict, 'channels', channel_name)
    inst_dict = set_v_for_k(inst_dict, 'offset', offset) 
    inst_dict = set_v_for_k(inst_dict, 'range_auto', range_auto)
    inst_dict = set_v_for_k(inst_dict, 'units', units)
    acq_dict = set_v_for_k(acq_dict, 'active_testplan_name', active_testplan_name)
    acq_dict = set_v_for_k(acq_dict, 'config_name', config_name)
    acq_dict = set_v_for_k(acq_dict, 'test_plan', test_plan)
    acq_dict = set_v_for_k(acq_dict, 'Start_TSE', (roundup(tse)))    
    bits = u2000(acq_dict,s)
    bits.transmitdec()
    bits.transmitraw()
    #bits.transmitblob()
    bits.testcomplete()
    post_status('Idle')
else:
    print "  FAILED: device not found (check your probe file)."

#post_status('Idle')
check_config_url()
