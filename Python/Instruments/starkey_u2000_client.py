#!/usr/bin/python2
"""Post status to monitor URL
>>> import ivi
>>> import new_u2000_client
>>> new_u2000_client.post_status("Testing")
result.reason= OK
result.status_code= 200
>>>
"""

import json
import requests
import time   # time is a module here
import datetime
from new_u2000_post import AgilentU2000
import ivi
import collections
import nuc_auth
from python_enum_usb import find_usb_devices

COMPANYNAME = 'Starkey'
HARDWARENAME = 'MSP1'
#GAE_INSTANCE = 'gradientone-test'
BASE_INSTANCE = 'https://starkey.gradientone.com'


def dt2ms(dtime):
    """Converts date time to miliseconds
    >>> from new_u2000_client import dt2ms
    >>> import datetime
    >>> dtime = datetime.datetime(2015, 12, 8, 18, 11, 44, 320012)
    >>> dt2ms(dtime)
    1449627104320
    """
    return int(dtime.strftime('%s'))*1000 + int(dtime.microsecond/1000)

def post_status(status, ses):
    "posts hardware status updates to the server"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    window = {'status':status, 'time':time.time()}
    status = json.dumps(window, ensure_ascii=True)
    # url_s = ("https://gradientone-test.appspot.com/status/"
    #          + COMPANYNAME + '/' + HARDWARENAME)
    #url_s = ("https://" + GAE_INSTANCE + ".appspot.com/status/"
    #        + COMPANYNAME + '/' + HARDWARENAME)
    url_s = BASE_INSTANCE + '/' + 'status' + '/' + 
            + COMPANYNAME + '/' + HARDWARENAME)
    result = requests.post(url_s, data=status, headers=headers)
    print "result.reason=", result.reason
    print "result.status_code=", result.status_code

def post_complete(config_name, active_testplan_name, ses):
    "posts information telling the server the test is complete"
    window_complete = {'commence_test':False}
    out_complete = json.dumps(window_complete, ensure_ascii=True)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # url_c = ("https://gradientone-test.appspot.com/temp_testcomplete/"
    #          + COMPANYNAME + '/' + config_name + '/'
    #          + active_testplan_name)
    # url_c = ("https://" + GAE_INSTANCE + ".appspot.com/temp_testcomplete/"
    #          + COMPANYNAME + '/' + config_name + '/'
    #          + active_testplan_name)
    url_c = BASE_INSTANCE + '/' + 'temp_testcomplete' + '/'
              + COMPANYNAME + '/' + config_name + '/'
              + active_testplan_name)
    result = ses.post(url_c, data=out_complete, headers=headers)
    print "result.reason=", result.reason
    print "result.status_code=", result.status_code

def check_config_vars(config, nested_config):
    "creates config variables to pass to the main u2000 code"
    if config['test_plan'] == 'True':
        active_testplan_name = config['active_testplan_name']
        config_name = config['config_name']
        #averaging_count_auto = nested_config['averaging_count_auto']
        correction_frequency = nested_config['correction_frequency']
        offset = nested_config['offset']
        range_auto = nested_config['range_auto']
        units = nested_config['units']
        pass_fail = nested_config['pass_fail']
        pass_fail_type = nested_config['pass_fail_type']
        max_value = nested_config['max_value']
        min_value = nested_config['min_value']
        test_plan = config['test_plan']
    else:
        active_testplan_name = config['active_testplan_name']
        test_plan = 'False'
        config_name = config['config_name']
        #averaging_count_auto = nested_config['averaging_count_auto']
        correction_frequency = nested_config['correction_frequency']
        offset = nested_config['offset']
        range_auto = nested_config['range_auto']
        units = nested_config['units']
        pass_fail = nested_config['pass_fail']
        pass_fail_type = nested_config['pass_fail_type']
        max_value = nested_config['max_value']
        min_value = nested_config['min_value']

    return (active_testplan_name, config_name, correction_frequency,
            offset, range_auto, units, test_plan, pass_fail,
            pass_fail_type, max_value, min_value)


def set_v_for_k(test_dict, key, val):
    "creates dictionary based off empty dictionary and key/value args"
    test_dict[key.encode('ascii')] = val
    return test_dict

def make_json(payload):
    "makes json based off input payload"
    acq_dict = json.dumps(payload)
    return acq_dict

def check_config_url():
    """polls the configuration URL for a start signal @ 1sec intervals"""
    #config_url = "http://localhost:18080/testplansummary/Acme/MSP"
    #config_url = ("https://gradientone-test.appspot.com/testplansummary/"
    #              + COMPANYNAME + '/' + HARDWARENAME)
    #config_url = ("https://gradientone-dev.appspot.com/
    #              testplansummary/Acme/MSP")
    #config_url = ("https://" + GAE_INSTANCE + ".appspot.com/testplansummary/"
    #              + COMPANYNAME + '/' + HARDWARENAME)
    config_url = BASE_INSTANCE + '/' + 'testplansummary' +'/'
                 + COMPANYNAME + '/' + HARDWARENAME
    # loop forever
    while True:
        token = nuc_auth.get_access_token()
        headers = {'Authorization': 'Bearer '+token}
        ses = requests.session()
        result = ses.get(config_url, headers=headers)
        if result.status_code == 401:
            token = nuc_auth.get_new_token()
            headers = {'Authorization': 'Bearer '+token}
            result = ses.get(config_url, headers=headers)
        if result:
            print 'checking'
            config = result.json()
            if config['configs_tps_traces']:
                nested_config = config['nested_config'][0]
                meas = config['meas'][0] 
                config = config['configs_tps_traces'][0]
                if config['commence_test'] == 'True':
                    print "Starting API"
                    post_status('Starting', ses)
                    u2000_acq(config, nested_config, meas, ses)
                    config_vars = check_config_vars(config, nested_config)
                    config_name = config_vars[1]
                    active_testplan_name = config_vars[0]
                    post_complete(config_name, active_testplan_name, ses)
            elif config['configs_run']:
                nested_config = config['nested_config'][0]
                config = config['configs_run'][0]
                print 'configs_runs config = ', config
                if config['commence_run'] == 'True':
                    print "Starting API" 
                    post_status('Starting', ses)
                    u2000_acq_run(config, nested_config, ses, headers)
            else:
                print "No start order found"
        find_usb_devices()
        time.sleep(1)


def u2000_acq_run(config, nested_config, ses, headers):
    """sets the configuration for the u2000 API and calls the u2000 class"""
    acq_dict = {}
    post_status('Acquiring', ses)
    print "Starting: Attempting to open one device..."
    #config_url = ("https://" + GAE_INSTANCE + ".appspot.com/testplansummary/"
    #              + COMPANYNAME + '/' + HARDWARENAME)
    config_url = BASE_INSTANCE + '/' + 'testplansummary' +'/'
                 + COMPANYNAME + '/' + HARDWARENAME
    u2000 = ivi.agilent.agilentU2001A(("USB::0x0957::0x2b18::INSTR"))
    while True:
        config_vars = check_config_vars(config, nested_config)
        u2000.channels['channel1'].correction_frequency = config_vars[2]
        u2000.channels['channel1'].offset = config_vars[3]
        #u2000.channels['channel1'].range_auto = config_vars[4]
        u2000.channels['channel1'].units = config_vars[5]
        #   initiate measurement
        u2000.measurement.initiate()
        # read out channel 1 power data
        power = u2000.measurement.fetch()
        tse = int(dt2ms(datetime.datetime.now()))
        inst_dict = {}
        inst_dict = set_v_for_k(inst_dict, 'correction_frequency', config_vars[2])
        inst_dict = set_v_for_k(inst_dict, 'pass_fail', config_vars[7])
        inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', config_vars[8])
        inst_dict = set_v_for_k(inst_dict, 'max_value', config_vars[9])
        inst_dict = set_v_for_k(inst_dict, 'min_value', config_vars[10])
        inst_dict = set_v_for_k(inst_dict, 'offset', config_vars[3])
        inst_dict = set_v_for_k(inst_dict, 'active_testplan_name', config_vars[0])
        inst_dict = set_v_for_k(inst_dict, 'test_plan', config_vars[6])
        acq_dict = collections.OrderedDict()
        acq_dict = set_v_for_k(acq_dict, 'Start_TSE', tse)
        acq_dict = set_v_for_k(acq_dict, 'data(dBm)', power)
        acq_dict = set_v_for_k(acq_dict, 'i_settings', inst_dict)
        acq_dict = set_v_for_k(acq_dict, 'config_name', config_vars[1])
        acq_dict = set_v_for_k(acq_dict, 'active_testplan_name', config_vars[0])
        acq_dict = set_v_for_k(acq_dict, 'test_plan', config_vars[6])
        bits = AgilentU2000(acq_dict, ses)
        bits.transmitraw()
        new_result = ses.get(config_url, headers=headers)
        new_config = new_result.json()
        if not new_config['configs_run']:
            print 'stopping'
            post_status('Idle', ses)
            break
    u2000.close()
        #post_status('Idle')



def u2000_acq(config, nested_config, meas, ses):
    """sets the configuration for the u2000 API and calls the u2000 class"""
    acq_dict = {}
    print "Starting: Attempting to open one device..."
    config_vars = check_config_vars(config, nested_config)
    u2000 = ivi.agilent.agilentU2001A(("USB::0x0957::0x2b18::INSTR"))
    #u2000.channels['channel1']
    u2000.channels['channel1'].correction_frequency = config_vars[2]
    u2000.channels['channel1'].offset = config_vars[3]
    #u2000.channels['channel1'].range_auto = config_vars[4]
    u2000.channels['channel1'].units = config_vars[5]
    #   initiate measurement
    u2000.measurement.initiate()
    # read out channel 1 power data
    post_status('Acquiring', ses)
    power = u2000.measurement.fetch()
    u2000.close()
    tse = int(dt2ms(datetime.datetime.now()))
    inst_dict = {}
    inst_dict = set_v_for_k(inst_dict, 'correction_frequency', config_vars[2])
    # inst_dict = set_v_for_k(inst_dict, 'pass_fail', config_vars[7])
    # inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', config_vars[8])
    # inst_dict = set_v_for_k(inst_dict, 'max_value', config_vars[9])
    # inst_dict = set_v_for_k(inst_dict, 'min_value', config_vars[10])
    if meas['default'] == 'True':
        inst_dict = set_v_for_k(inst_dict, 'pass_fail', meas['pass_fail'])
        inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', 'Range') #needs more work, range is a placeholder
        inst_dict = set_v_for_k(inst_dict, 'max_value', meas['max_pass'])
        inst_dict = set_v_for_k(inst_dict, 'min_value', meas['min_pass'])
    else:
        inst_dict = set_v_for_k(inst_dict, 'pass_fail', 'N/A')
        inst_dict = set_v_for_k(inst_dict, 'pass_fail_type', 'N/A') #needs more work, range is a placeholder
        inst_dict = set_v_for_k(inst_dict, 'max_value', 0.0)
        inst_dict = set_v_for_k(inst_dict, 'min_value', 0.0)
    inst_dict = set_v_for_k(inst_dict, 'offset', config_vars[3])
    inst_dict = set_v_for_k(inst_dict, 'active_testplan_name', config_vars[0])
    inst_dict = set_v_for_k(inst_dict, 'test_plan', config_vars[6])
    print inst_dict
    acq_dict = collections.OrderedDict()
    acq_dict = set_v_for_k(acq_dict, 'Start_TSE', tse)
    acq_dict = set_v_for_k(acq_dict, 'data(dBm)', power)
    acq_dict = set_v_for_k(acq_dict, 'i_settings', inst_dict)
    acq_dict = set_v_for_k(acq_dict, 'config_name', config_vars[1])
    acq_dict = set_v_for_k(acq_dict, 'active_testplan_name', config_vars[0])
    acq_dict = set_v_for_k(acq_dict, 'test_plan', config_vars[6])
    print acq_dict
    bits = AgilentU2000(acq_dict, ses)
    bits.transmitraw()
    bits.transmitblob()
    bits.testcomplete()
    post_status('Idle', ses)




# To test, use "export TEST_U2000_CLIENT=1"
# To stop testing, "unset TEST_U2000_CLIENT"

if __name__ == "__main__":
    import os
    if not 'TEST_U2000_CLIENT' in os.environ:
        check_config_url()
    else:
        import doctest
        print "running doctest"
        doctest.testmod()
        print "doctest complete"
        #print "TestResults =", doctest.TestResults  # later

