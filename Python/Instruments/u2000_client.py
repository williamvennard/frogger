import json
import requests
import grequests
import time   # time is a module here
import math
import datetime
import threading
from u2000_post import agilentu2000
import numpy as np
import numpy.fft as fft
import scipy.signal 
import ivi
import usb
import nuc_auth

COMPANYNAME = 'Acme'
HARDWARENAME = 'Tahoe'
GAE_INSTANCE = 'gradientone-dev2'

def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

def post_status(status):
    "posts hardware status updates to the server"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    window = {'status':status, 'time':time.time()}
    status = json.dumps(window, ensure_ascii=True)
    # url_s = "https://gradientone-test.appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
    url_s = "https://" + GAE_INSTANCE + ".appspot.com/status/" + COMPANYNAME + '/' + HARDWARENAME
    s = requests.post(url_s, data=status, headers=headers)
    print "s.reason=",s.reason
    print "s.status_code=",s.status_code
    #print "dir(s)=",dir(s)

def post_complete(config_name, active_testplan_name, s):
    window_complete = {'commence_test':False}
    out_complete = json.dumps(window_complete, ensure_ascii=True)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # url_c = "https://gradientone-test.appspot.com/temp_testcomplete/" + COMPANYNAME + '/' + config_name + '/' + active_testplan_name
    url_c = "https://" + GAE_INSTANCE + ".appspot.com/temp_testcomplete/" + COMPANYNAME + '/' + config_name + '/' + active_testplan_name
    c = s.post(url_c, data=out_complete, headers=headers)
    print "c.reason=",c.reason
    print "c.status_code=",c.status_code
    #print "dir(c)=",dir(c)

def check_config_vars(config, nested_config):
    "creates config variables to pass to the main u2000 code"
    if config['test_plan'] == 'True':
        active_testplan_name = config['active_testplan_name']
        config_name = config['config_name']
        averaging_count_auto = config['averaging_count_auto']
        correction_frequency= config['correction_frequency']
        offset= config['offset']
        range_auto= config['range_auto']
        units= config['units']
        test_plan =config['test_plan']
    else:
        active_testplan_name = config['active_testplan_name']
        test_plan = 'False'
        config_name = config['config_name']
        averaging_count_auto = nested_config['averaging_count_auto']
        correction_frequency= nested_config['correction_frequency']
        offset= nested_config['offset']
        range_auto= nested_config['range_auto']
        units= nested_config['units']
        pass_fail = nested_config['pass_fail']
        pass_fail_type = nested_config['pass_fail_type']
        max_value = nested_config['max_value']
        min_value = nested_config['min_value']


    return active_testplan_name, config_name, correction_frequency, offset, range_auto, units, test_plan, pass_fail, pass_fail_type, max_value, min_value



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
    #config_url = "http://localhost:18080/testplansummary/Acme/MSP"
    #config_url = "https://gradientone-test.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    #config_url = "https://gradientone-dev.appspot.com/testplansummary/Acme/MSP"
    config_url = "https://" + GAE_INSTANCE + ".appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    token = nuc_auth.get_access_token()
    headers = {'Authorization': 'Bearer '+token}
    s = requests.session()
    r = s.get(config_url, headers=headers)
    if r.status_code == 401:
        token = nuc_auth.get_new_token()
        headers = {'Authorization': 'Bearer '+token}
        r = s.get(config_url, headers=headrs)
    if r:
        print 'checking'
        config = r.json()
        if config['configs_tps_traces']:
            nested_config = config['nested_config'][0]
            config = config['configs_tps_traces'][0]
            measurements = config['measurements'][0]
            if config['commence_test'] == 'True':  
                print "Starting API"
                post_status('Starting')
                u2000_acq(config, nested_config, measurements, s)
                config_vars = check_config_vars(config, nested_config)
                config_name = config_vars[1]
                active_testplan_name = config_vars[0]
                post_complete(config_name, active_testplan_name, s)
        else:
            print "No start order found"
    threading.Timer(1, check_config_url()).start()


def u2000_acq(config, nested_config, measurements, s):    
    """sets the configuration for the u2000 API and calls the u2000 class"""
    time_start = time.time()
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    config_vars = check_config_vars(config, nested_config)
    u2000 = get_u2000_device()
    u2000.channels['channel1']
    u2000.channels['channel1'].correction_frequency = config_vars[2]
    #u2000.channels['channel1'].offset = config_vars[3]
    #u2000.channels['channel1'].range_auto = config_vars[4]
    #u2000.channels['channel1'].units = config_vars[5]
    #   initiate measurement
    u2000.measurement.initiate()
    # read out channel 1 power data
    #post_status('Acquiring')
    power = u2000.measurement.fetch()
    u2000.close()
    del u2000
    tse = dt2ms(datetime.datetime.now())
    config_dict = {}
    plot_dict = {}
    inst_dict = {}
    inst_dict = set_v_for_k(inst_dict, 'correction_frequency', config_vars[2])
    inst_dict = set_v_for_k(inst_dict, 'pass_fail', config_vars[7])
    inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', config_vars[8])
    inst_dict = set_v_for_k(inst_dict, 'max_value', config_vars[9])
    inst_dict = set_v_for_k(inst_dict, 'min_value', config_vars[10])
    # inst_dict = set_v_for_k(inst_dict, 'pass_fail', measurements['pass_fail'])
    # inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', measurements['pass_fail_type'])
    # inst_dict = set_v_for_k(inst_dict, 'max_value', measurements['max_value'])
    # inst_dict = set_v_for_k(inst_dict, 'min_value', measurements['min_value'])
    acq_dict = set_v_for_k(acq_dict, 'i_settings', inst_dict)    
    acq_dict = set_v_for_k(acq_dict, 'config_name', config_vars[1]) 
    acq_dict = set_v_for_k(acq_dict, 'active_testplan_name', config_vars[0])
    acq_dict = set_v_for_k(acq_dict, 'test_plan', config_vars[6])
    acq_dict = set_v_for_k(acq_dict, 'Start_TSE', tse) 
    acq_dict = set_v_for_k(acq_dict, 'data', power)  
    print acq_dict
    bits = agilentu2000(acq_dict,s)
    bits.transmitraw()
    bits.transmitblob()
    bits.testcomplete()
    #post_status('Idle')
    time.sleep(5)

#post_status('Idle')
check_config_url()

