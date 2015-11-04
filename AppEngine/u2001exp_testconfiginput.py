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
        self.render('testconfig.html', dropdown = dropdown)

    def post(self):
        testplan_object = json.loads(self.request.body)
        print testplan_object
        configs = []
        testplan_name = testplan_object['testplan_name']
        author = testplan_object['author']
        company_nickname = testplan_object['company_nickname']
        order = testplan_object['order']
        order = [item.encode("ascii") for item in order]
        duts = testplan_object['duts']
        measurements = testplan_object['meas']
        configs = testplan_object['configs']
        start_now = testplan_object['start_now']
        start_time = testplan_object['start_time']
        checkbox_names = ["start_measurement_now"]
        # averaging_count_auto= testplan_object['averaging_count_auto']
        # correction_frequency = testplan_object['correction_frequency']
        # offset = testplan_object['offset']
        # range_auto = testplan_object['range_auto']
        # units = testplan_object['units']
        # max_value = testplan_object['max_value']
        # min_value = testplan_object['min_value']
        # pass_fail = testplan_object['pass_fail']
        # pass_fail_type = testplan_object['pass_fail_type']
        if start_now == True:
            date_object = datetime.datetime.now()
        else:
            date_object = datetime.datetime.fromtimestamp(int(start_time)/1000)
        t = TestDB(key_name = testplan_name, parent = company_key(),
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            order = order,
            test_plan = True,
            trace = False,
            scheduled_start_time = date_object,
            test_ready = True,
            test_scheduled = True,
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
            meas = MeasurementDB.gql("Where meas_name =:1", item['meas_name']).get()
            if meas == None:  #if there is not an instrument with the inputted name, then create it in the DB
                m = MeasurementDB(key_name = item['meas_name'], parent = company_key(),
                company_nickname = company_nickname, author = author,
                meas_type = item['meas_type'],
                meas_name = item['meas_name'],             
                meas_start_time = float(item['meas_stop_time']),
                meas_stop_time = float(item['meas_stop_time']),
                )
                m.put()
            key = db.Key.from_path('MeasurementDB', item['meas_name'], parent = company_key())
            measurement = db.get(key)
            if test.key() not in measurement.tests:  #add the test plan to the list property of the dut
                measurement.tests.append(test.key())
                measurement.put()
            if measurement.key() not in test.measurements:  #add the  dut name to the list property ot the test plan
                test.measurements.append(measurement.key())
                test.put()    
        for item in configs:
            config = ConfigDB.gql("Where config_name =:1", item['config_name']).get()
            if config == None:  #if there is not an instrument with the inputted name, then create it in the DB
                if config_inst_type == 'U2001A':
                    c = ConfigDB(key_name = (item['config_name']+testplan_name), parent = company_key(),
                    company_nickname = company_nickname, 
                    author = author,
                    instrument_type = item['instrument_type'],
                    hardware_name = item['hardware'],
                    test_plan = True,
                    active_testplan_name = testplan_name,
                    commence_test = False,
                    trace = False,
                    )
                    c.put()
                    s = agilentU2000(key_name = (config_name+instrument_type), parent = company_key(),
                    config_name = config_name,
                    company_nickname = company_nickname, 
                    hardware_name = hardware_name, 
                    instrument_type = instrument_type,
                    averaging_count_auto = averaging_count_auto, 
                    correction_frequency = correction_frequency, 
                    offset = offset, 
                    range_auto = range_auto, 
                    units = units,
                    max_value = max_value,
                    min_value = min_value,
                    pass_fail = pass_fail,
                    pass_fail_type = pass_fail_type,
                    )
                    s.put() 
                else:
                    c = ConfigDB(key_name = (item['config_name']+testplan_name), parent = company_key(),
                    company_nickname = company_nickname, author = author,
                    analog_bandwidth = item['analog_bandwidth'],
                    capture_channels = item['capture_channels'],
                    analog_sample_rate = item['analog_sample_rate'],
                    resolution = item['resolution'],
                    capture_buffer_size = item['capture_buffer_size'],
                    instrument_type = item['instrument_type'],
                    hardware_name = item['hardware'],
                    test_plan = True,
                    active_testplan_name = testplan_name,
                    trace = False,
                    )
                    c.put()
            key = db.Key.from_path('ConfigDB', (item['config_name']+testplan_name), parent = company_key())
            configuration = db.get(key)
            if test.key() not in configuration.tests:  #add the test plan to the list property of the dut
                configuration.tests.append(test.key())
                configuration.put()
            if configuration.key() not in test.configs:  #add the  dut name to the list property ot the test plan
                test.configs.append(configuration.key())
                test.put()    

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