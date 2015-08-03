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
from datetime import datetime
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
        print testplan_object
        print type(testplan_object)
        configs = []
        testplan_name = testplan_object['testplan_name']
        author = testplan_object['author']
        company_nickname = testplan_object['company_nickname']
        order = testplan_object['order']

        duts = testplan_object['duts']
        measurements = testplan_object['meas']
        configs = testplan_object['configs']
        start_now = testplan_object['start_now']
        
        #config_name = self.request.get('config_name')
        #analog_bandwidth = self.request.get('analog_bandwidth')
        #analog_sample_rate = self.request.get('analog_sample_rate')
        #capture_buffer_size = self.request.get('capture_buffer_size')
        #capture_channels = self.request.get('capture_channels')
        #resolution = self.request.get('resolution')
        
        #dut_name = self.request.get('dut_name')
        #meas_type = self.request.get('meas_type')
        #meas_name = self.request.get('meas_name')
        #meas_start_time = self.request.get('meas_start_time')
        #meas_stop_time = self.request.get('meas_stop_time')
        #dut_type = self.request.get('dut_type')
        #settings = self.request.get('settings')


        if testpost == 'True': #this controls the POST functionality if someone is configuring test plan details.
            t = TestDB(key_name = testplan_name, parent = company_key(),
            testplan_name = testplan_name, 
            company_nickname = company_nickname, 
            author = author,
            test_plan = True,
            trace = False,
            test_ready = False,
            test_scheduled = False
            )
            t.put() 
            self.render('testconfig.html', testplan_name = testplan_name)
        if confpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            insts_and_explanations = instruments_and_explanations(analog_bandwidth, analog_sample_rate, capture_buffer_size, capture_channels, resolution)
            instruments = insts_and_explanations[0]
            explanations = insts_and_explanations[-1]
            avail = []
            for inst in instruments:
                i = (InstrumentsDB.gql("Where instrument_type =:1", inst))
                for entry in i:
                    avail.append((inst, entry.hardware_name))
            if len(avail) == 0:
                selected_inst_type = "None Selected"
                selected_hardware = "None Selected"
                avail = "None available"
            else:
                selected_inst_type = avail[0][0]
                selected_hardware = avail[0][1]
                avail = avail
            self.render('testconfig.html', explanations = explanations, selected_inst_type = selected_inst_type, selected_hardware = selected_hardware, avail_inst = avail)
        if dutpost == 'True': #this controls the POST functionality if someone is configuring instrument details.
            test_order = self.request.get('dut_test_order')
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            dut = DutDB.gql("Where dut_name =:1", dut_name).get()
            if dut == None:  #if there is not an instrument with the inputted name, then create it in the DB
                d = DutDB(key_name = dut_name, parent = company_key(),
                    company_nickname = company_nickname, author = author,
                    dut_type = dut_type,
                    dut_name = dut_name,             
                    settings = settings,
                    )
                d.put()
            dut_order = 'dut'+':'+dut_name+':'+test_order
            print dut_order  
            test.order.append(dut_order)
            test.put()
            key = db.Key.from_path('DutDB', dut_name, parent = company_key())
            dut = db.get(key)
            if test.key() not in dut.tests:  #add the test plan to the list property of the dut
                dut.tests.append(test.key())
                dut.put()
            if dut.key() not in test.duts:  #add the  dut name to the list property ot the test plan
                test.duts.append(dut.key())
                test.put()    
            #self.render('testconfig.html')
        if selectpost == 'True':
            instrument_type = self.request.get('selected_inst_type')
            hardware_name = self.request.get('selected_hardware')
            test_order = self.request.get('config_test_order')
            testplan_name = self.request.get('testplan_name')
            print config_name, instrument_type, hardware_name, testplan_name
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            c = ConfigDB(key_name = config_name, parent = company_key(), company_nickname = company_nickname, author = author,
                    hardware_name = hardware_name, instrument_type = instrument_type,
                    config_name = config_name,             
                    test_plan = True,
                    trace = False,
                    number_of_samples = 100,
                    sample_rate = 32000,
                    )
            c.put()
            config_order = 'config'+':'+config_name+':'+test_order 
            test.order.append(config_order)
            test.put()
            key = db.Key.from_path('ConfigDB', config_name, parent = company_key())
            conf = db.get(key)
            if test.key() not in conf.tests:  #add the test plan to the list property of the instrument
                conf.tests.append(test.key())
                conf.put()
            if conf.key() not in test.configs:  #add the instrument name to the list property ot the test plan
                test.configs.append(conf.key())
                test.put()
            self.render('testconfig.html')
        if measpost == 'True': #this controls the POST functionality if someone is configuring measurement details.
            meas_order = self.request.get('meas_test_order')
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            meas = MeasurementDB.gql("Where dut_name =:1", meas_name).get()
            #print meas_type, meas_name, author, company_nickname, meas_start_time, meas_stop_time
            if meas == None:  #if there is not an instrument with the inputted name, then create it in the DB
                m = MeasurementDB(key_name = meas_name, parent = company_key(),
                    company_nickname = company_nickname, author = author,
                    meas_type = meas_type,
                    meas_name = meas_name,             
                    meas_start_time = float(meas_stop_time),
                    meas_stop_time = float(meas_stop_time),
                    )
                m.put()
            meas_order = 'meas'+':'+meas_name+':'+meas_order
            test.order.append(meas_order)
            test.put()
            key = db.Key.from_path('MeasurementDB', meas_name, parent = company_key())
            measurement = db.get(key)
            if test.key() not in measurement.tests:  #add the test plan to the list property of the dut
                measurement.tests.append(test.key())
                measurement.put()
            if measurement.key() not in test.measurements:  #add the  dut name to the list property ot the test plan
                test.measurements.append(measurement.key())
                test.put()    
            self.render('testconfig.html')


        if timepost == 'True':
            testplan_name = self.request.get('testplan_name')
            company_nickname = self.request.get('company_nickname')
            start_time = str(self.request.get('start_time'))
            checkbox_names = ["start_measurement_now"]
            start_measurement_now = self.request.get('start_measurement_now')
            if start_measurement_now == 'on':
                date_object = datetime.now()
            else:
                date_object = datetime.strptime(start_time, '%b %d %Y %I:%M%p')
            test = TestDB.gql("Where testplan_name =:1", testplan_name).get()
            test.scheduled_start_time = date_object
            test.test_ready = True
            test.test_scheduled = True
            test.put()
            taskqueue.add(url = '/testmanager', method = 'POST', params={'info':(company_nickname,testplan_name)}, eta = date_object)
                       
        #self.redirect('/testplansummary/' + company_nickname + '/' + hardware_name)