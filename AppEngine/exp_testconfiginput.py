from gradientone import InstrumentDataHandler
from gradientone import render_json
from gradientone import author_creation
from gradientone import query_to_dict
from gradientone import is_checked
from gradientone import instruments_and_explanations
from onedb import ConfigDB
from onedb import company_key
from onedb import TestDB
from onedb import DutDB
from onedb import CapabilitiesDB
from onedb import InstrumentsDB
from onedb import MeasurementDB
from onedb import MeasurementDB_key
from onedb import agilentU2000
import datetime
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import taskqueue
import appengine_config

class Handler(InstrumentDataHandler):
    def get(self):
        #if not self.authcheck():
        #    return
        c = db.GqlQuery("""SELECT * FROM ConfigDB""")
        rows_c = list(c)
        dropdown = query_to_dict(rows_c)
        print dropdown
        self.render('exp_testconfig.html', dropdown = dropdown)

    def post(self):
        testplan_object = json.loads(self.request.body)
        print "TESTPLAN OBJECT: ", testplan_object
        configs = []
        testplan_name = testplan_object['testplan_name']
        author = testplan_object['author']
        company_nickname = testplan_object['company_nickname']
        hardware_name = testplan_object['hardware_name']
        order = testplan_object['order']
        order = [item.encode("ascii") for item in order]  # temporarily comment out to support dummy u2000 config data
        #order = ['config:mmm1:0', 'config:mmm2:1']
        duts = testplan_object['duts']
        measurements = testplan_object['meas']
        print "CONFIG FROM TESTPLAN OBJECT:", testplan_object['configs']
        configs = testplan_object['configs']  # previously temporarily comment out to support dummy u2000 config data below
        #configs = [{u'instrument_type': u'U2001A', u'config_name': u'dummy',  u'hardware': u'MSP',u'range_auto': u'True',  u'units': u'dBm', u'offset': u'0.0',u'averaging_count_auto': u'True', u'correction_frequency': u'1e9'}]
        start_now = testplan_object['start_now']
        start_time = testplan_object['start_time']
        checkbox_names = ["start_measurement_now"]
        ops_start = testplan_object['ops_start']
        if ops_start:
            date_object = None
        elif start_now:
            date_object = datetime.datetime.now()
        else:
            date_object = datetime.datetime.fromtimestamp(int(start_time)/1000)
        t = TestDB(key_name = testplan_name, parent = company_key(),
            testplan_name = testplan_name, 
            company_nickname = company_nickname,
            hardware_name = hardware_name, 
            author = author,
            order = order,
            test_plan = True,
            trace = False,
            scheduled_start_time = date_object,
            test_ready = True,
            test_scheduled = True,
            ops_start = ops_start,
            )
        t.put() 
        key = db.Key.from_path('TestDB', testplan_name, parent = company_key())
        test = db.get(key)
        for item in duts:
            dut = DutDB.gql("Where dut_name =:1", item['dut_name']).get()
            if dut == None:  #if there is not an instrument with the inputted name, then create it in the DB
                d = DutDB(key_name = item['dut_name'], parent = company_key(),
                company_nickname = company_nickname, author = author,
                dut_type = item['dut_type'],
                dut_name = item['dut_name'],             
                settings = item['settings'],
                )
                d.put()
            key = db.Key.from_path('DutDB', item['dut_name'], parent = company_key())
            dut = db.get(key)
            if test.key() not in dut.tests:  #add the test plan to the list property of the dut
                dut.tests.append(test.key())
                dut.put()
            if dut.key() not in test.duts:  #add the  dut name to the list property ot the test plan
                test.duts.append(dut.key())
                test.put()    
        
        for item in measurements:
            meas = MeasurementDB.get(MeasurementDB_key(item['meas_name']))
            if meas == None:  #if there is not a measurement with the inputted name, then create it in the DB
                meas = MeasurementDB(key_name = item['meas_name'], parent = company_key(),
                company_nickname = company_nickname, author = author,
                # meas_type = item['meas_type'],
                meas_type = 'basic',
                meas_name = item['meas_name'],             
                # meas_start_time = float(item['meas_stop_time']),
                # meas_stop_time = float(item['meas_stop_time']),
                pass_fail = bool(item['pass_fail']),
                min_pass = float(item['min_value']),
                max_pass = float(item['max_value']),
                )
                meas.put()
            if test.key() not in meas.tests:
                meas.tests.append(test.key())
                meas.put()
            if meas.key() not in test.measurements:
                test.measurements.append(meas.key())
                test.put()
                   
        for item in configs:
            config = ConfigDB.gql("Where config_name =:1", item['config_name']).get()
            if config == None:  #if there is not an instrument with the inputted name, then create it in the DB
                # c = ConfigDB(key_name = (item['config_name']+testplan_name), parent = company_key(),
                # company_nickname = company_nickname, author = author,
                # analog_bandwidth = item['analog_bandwidth'],
                # capture_channels = int(item['capture_channels']),
                # analog_sample_rate = int(item['analog_sample_rate']),
                # resolution = item['resolution'],
                # capture_buffer_size = int(item['capture_buffer_size']),
                # instrument_type = item['instrument_type'],
                # hardware_name = item['hardware'],
                # test_plan = True,
                # active_testplan_name = testplan_name,
                # trace = False,
                # config_name = item['config_name'],
                # )
                # c.put()
                config = ConfigDB(key_name = (item['config_name']+testplan_name), parent = company_key(),
                company_nickname = company_nickname, 
                author = author,
                instrument_type = item['instrument_type'],
                hardware_name = item['hardware'],
                test_plan = True,
                active_testplan_name = testplan_name,
                commence_test = False,
                trace = False,
                config_name = item['config_name'],
                )
                config.put()

                if item['instrument_type'] == "U2001A":
                    print 'item =', item
                    pass_fail = item['pass_fail']
                    max_value = float(item['max_value'])
                    min_value = float(item['min_value'])
                    print pass_fail, max_value, min_value
                    s = agilentU2000(key_name = (item['config_name']+item['instrument_type']), parent = company_key(),
                    config_name = item['config_name'],
                    company_nickname = company_nickname, 
                    hardware_name = item['hardware'], 
                    instrument_type = item['instrument_type'],
                    averaging_count_auto = item['averaging_count_auto'], 
                    correction_frequency = item['correction_frequency'], 
                    offset = item['offset'], 
                    range_auto = item['range_auto'], 
                    units = item['units'],
                    max_value = max_value,
                    min_value = min_value,
                    pass_fail = pass_fail,
                    pass_fail_type = '',
                    )
                    s.put()
                    if s.key() not in test.instrument_configs:
                        test.instrument_configs.append(s.key())
                        test.put()
            if test.key() not in config.tests:  #add the test plan to the list property of the dut
                config.tests.append(test.key())
                config.put()
            if config.key() not in test.configs:  #add the  dut name to the list property ot the test plan
                test.configs.append(config.key())
                test.put()
        if date_object:    
            taskqueue.add(url = '/testmanager', method = 'POST', params={'info':(company_nickname,testplan_name)}, eta = date_object)
                       
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)

       # instrument_type = self.request.get('selected_inst_type')
       # hardware_name = self.request.get('selected_hardware')
       # test_order = self.request.get('config_test_order')
       # testplan_name = self.request.get('testplan_name')
       # print config_name, instrument_type, hardware_name, testplan_name
       # test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
       # c = ConfigDB(key_name = config_name, parent = company_key(), company_nickname = company_nickname, author = author,
       #         hardware_name = hardware_name, instrument_type = instrument_type,
       #         config_name = config_name,             
       #         test_plan = True,
       #         trace = False,
       #         number_of_samples = 100,
       #         sample_rate = 32000,
       #         )
       # c.put()
       # config_order = 'config'+':'+config_name+':'+test_order 
       # test.order.append(config_order)
       # test.put()
       # key = db.Key.from_path('ConfigDB', config_name, parent = company_key())
       # conf = db.get(key)
       # if test.key() not in conf.tests:  #add the test plan to the list property of the instrument
       #     conf.tests.append(test.key())
       #     conf.put()
       # if conf.key() not in test.configs:  #add the instrument name to the list property ot the test plan
       #     test.configs.append(conf.key())
       #     test.put()

        #insts_and_explanations = instruments_and_explanations(analog_bandwidth, analog_sample_rate, capture_buffer_size, capture_channels, resolution)
        #instruments = insts_and_explanations[0]
        #explanations = insts_and_explanations[-1]
        #avail = []
        #for inst in instruments:
        #    i = (InstrumentsDB.gql("Where instrument_type =:1", inst))
        #    for entry in i:
        #        avail.append((inst, entry.hardware_name))
        #if len(avail) == 0:
        #    selected_inst_type = "None Selected"
        #    selected_hardware = "None Selected"
        #    avail = "None available"
        #else:
        #    selected_inst_type = avail[0][0]
        #    selected_hardware = avail[0][1]
        #    avail = avail
        #    self.render('testconfig.html', explanations = explanations, selected_inst_type = selected_inst_type, selected_hardware = selected_hardware, avail_inst = avail)