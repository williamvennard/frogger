import time
import datetime 
import math
import itertools
import json
import requests

s = requests.session()
u = "https://gradientone-prod.appspot.com/testplansummary/Acme/Tahoe"
r = s.get(u)


loop = range(0, 100)

for l in loop:
    time.sleep(0.2)
    start_time = time.time()
    parent = 'raw'
    stuffing = {'start_tse': 1437068057100, 'cha': '[1.71875, 1.67578125, 1.67578125, 1.6328125, 1.6328125, 1.6328125, 1.67578125, 1.71875, 1.71875, 1.76171875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.76171875, 1.71875, 1.71875, 1.67578125, 1.67578125, 1.67578125, 1.6328125, 1.67578125, 1.71875, 1.71875, 1.71875, 1.76171875, 1.8046875, 1.8046875, 1.76171875, 1.8046875, 1.76171875, 1.76171875, 1.76171875, 1.71875, 1.67578125, 1.6328125, 1.67578125, 1.67578125, 1.67578125, 1.71875, 1.71875, 1.71875, 1.8046875, 1.8046875, 1.76171875, 1.8046875, 1.8046875, 1.76171875, 1.71875, 1.71875, 1.67578125, 1.6328125, 1.6328125, 1.67578125, 1.6328125, 1.67578125, 1.71875, 1.71875, 1.76171875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.71875, 1.71875, 1.71875, 1.67578125, 1.67578125, 1.67578125, 1.6328125, 1.67578125, 1.71875, 1.71875, 1.76171875, 1.76171875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.76171875, 1.71875, 1.71875, 1.71875, 1.67578125, 1.67578125, 1.67578125, 1.67578125, 1.6328125, 1.71875, 1.71875, 1.76171875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.8046875, 1.76171875, 1.71875]', 'i_settings': {'BitScope': ['BS000501', 'KD58VM58'], 'Library': ['2.0 FE26A', 'Python DC01L'], 'Channels': [10, 2, 8], 'Sample_Size': 200, 'Link': 'USB:/dev/ttyUSB0', 'Sample_Rate_Hz': 1000.0}, 'testplan_name': u'addone', 'p_settings': {'Total_Slices': 2, 'Start_TSE': '1437068057100', 'Dec_msec_btw_samples': 10, 'Raw_msec_btw_samples': 1, 'Slice_Size_msec': 100}, 'slicename': 1437068057100}
    window_bscope = {'cha':stuffing, 'start_tse':'143706857100'}
    out_bscope = json.dumps(window_bscope, ensure_ascii=True)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if parent == 'raw':    
            #url = "http://localhost:18080/bscopedata/arduino/%s" % slicename
        url_b = "https://gradientone-prod.appspot.com/bscopedata/Acme/Tahoe/mac/143706857100" 
    else:
            #url = "http://localhost:18080/dec/bscopedata/arduino/%s" % slicename
        url_b = "https://gradientone-prod.appspot.com/bscopedata/Acme/Tahoe/mac/143706857100" 
    b4_post = time.time()
    r = s.post(url_b, data=out_bscope, headers=headers)
    after_post = time.time()
    #print "dir(r)=",dir(r)
    print "r.reason=",r.reason
    print "r.status_code=",r.status_code
    finish_time = time.time()
    thru_post = b4_post - start_time
    total_post = after_post - b4_post
    response = finish_time - after_post
    total_time = finish_time - start_time

    print 'thru post', thru_post
    print 'total post', total_post
    print 'response codes', response
    print 'total time', total_time