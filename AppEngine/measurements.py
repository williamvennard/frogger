import webapp2
import jinja2
import json
import logging
import os
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
from onedb import CapabilitiesDB
from onedb import ProfileDB
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
import hashlib
import math
import numpy as np
import decimate

def measurement_config(i_settings, value):
    if i_settings['pass_fail'] = 'True':
        if i_settings['pass_fail_type'] = 'max_min':
            measurement_result = max_min(i_settings['max_value'], i_settings['min_val'],value)
    else:
        measurement_result = 'No Measurement Defined'
    return measurement_result


    {'max_value': '25', 'min_value': '2', 'pass_fail_type': 'max_min', 'pass_fail': 'True', 'correction_frequency': '0.0'}

def max_min(max_val, min_val, value):
    if min_val <= value <= max_val:
        max_min_result = 'Pass'
    else:
        max_min_result = 'Fail'
    return max_min_result

def threshold(threshold, value):
    if value >= threshold:
        threshold_result = 'Pass'
    else:
        threshold_result = 'Fail'
    return threshold_result











def root_mean_squared_ta(test_data, RMS_time_start, RMS_time_stop, sample_interval):
    "RMS measurement function (for ideal sine wave) that relies upon user input for start/stop time and sample interval from the config"
    RMS_time_start = float(RMS_time_start)
    RMS_time_stop = float(RMS_time_stop) 
    sum = 0
    tempsq = 0
    i = 0
    for entry in test_data[int(RMS_time_start/sample_interval):(1+int(RMS_time_stop/sample_interval))]:
        tempsq = entry*entry
        sum += tempsq 
        i += 1  
    z = sum/i
    rms = math.sqrt(z)
    return rms

def peak_voltage_ta(test_data, RMS_time_start, RMS_time_stop, sample_interval):
    "Peak voltage measurement function (for ideal sine wave) that relies upon user input for start/stop time and sample interval from the config"
    RMS_time_start = float(RMS_time_start)
    RMS_time_stop = float(RMS_time_stop) 
    sum = 0
    tempsq = 0
    i = 0
    for entry in test_data[int(RMS_time_start/sample_interval):(1+int(RMS_time_stop/sample_interval))]:
        tempsq = entry*entry
        sum += tempsq 
        i += 1  
    z = sum/i
    peak_voltage = math.sqrt(z) * 1.414
    return peak_voltage

def peak_to_peak_voltage_ta(test_data, time_start, time_stop, sample_interval):
    "Peak to Peak measurement function (for ideal sine wave) that relies upon user input for start/stop time and sample interval from the config"
    time_start = float(time_start)
    time_stop = float(time_stop) 
    sum = 0
    tempsq = 0
    i = 0
    for entry in test_data[int(time_start/sample_interval):(1+int(time_stop/sample_interval))]:
        tempsq = entry*entry
        sum += tempsq 
        i += 1  
    z = sum/i
    peak_to_peak_voltage = math.sqrt(z)*2*math.sqrt(2)
    return peak_to_peak_voltage

def create_decimation(data):
    new_results = []
    for d in data:
        entries = d['cha'].split(',')
        for entry in entries:
            entry = entry.lstrip('[')
            entry = entry.rstrip(']')
            new_results.append(float(entry))
    new_results = new_results[:1000]
    results_arr = np.array(new_results)  #puts the test data in an array
    dec = decimate.decimate(results_arr, 10, ftype='fir', axis=0)  #performs the decimation function
    test_results = dec.tolist()
    return test_results