from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
from onedb import Scope
from onedb import agilentBaseScope
from onedb import agilentBaseInfiniiVision
from onedb import agilent7000
from onedb import agilent7000A
from onedb import agilentMSO7014A
from onedb import agilentU2000data
import jinja2
import json
import logging
import webapp2
import numpy
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
#from send_script_post import Script


class Handler(InstrumentDataHandler):
    def get(self, company_nickname="", config_name=""):
        # user = users.get_current_user()
        # if user:
        #     active_user = user.email()
        #     active_user= active_user.split('@')
        #     author = active_user[0]
        # else:
        #     self.redirect(users.create_login_url(self.request.uri))
        # instrument_name = instrument_name.split('.')
        # if instrument_name[-1] == 'json':
        #     rows = db.GqlQuery("""SELECT * FROM ConfigDB WHERE author =:1 
        #                         and instrument_type =:2 
        #                         and instrument_name =:3""", 
        #                         author, instrument_type, instrument_name[0])
        #     inst_config = [r.to_dict() for r in rows]
        #     rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE 
        #                         name ='default-scope' ORDER BY TIME ASC""")
        #     default_data = [r.to_dict() for r in rows]
        #     inst_default = {"data":default_data, "inst_config":inst_config}
        #     render_json(self, inst_default)
        # elif author and instrument_type and instrument_name:
        #     rows_inst_details = db.GqlQuery("""SELECT * FROM ConfigDB WHERE
        #                                      author =:1 and instrument_type 
        #                                      =:2 and instrument_name =:3""", 
        #                                      author, instrument_type, 
        #                                      instrument_name[0])
        #     self.render('instrument_detail.html')
        # else:
        print company_nickname, config_name
        rows = db.GqlQuery("SELECT * FROM agilentU2000data WHERE company_nickname =:1 and config_name =:2", company_nickname, config_name)
        rows = query_to_dict(rows)
        meas_results = []
        meas_results_calcs = []
        for entry in rows:
            meas_results.append((float(entry['test_results_data']), config_name, entry['i_settings'], ("https://gradientone-test.appspot.com/u2000data/" + company_nickname + '/' + entry['hardware_name'] +'/' + config_name + "/%s" % entry['start_tse'])))
            meas_results_calcs.append(float(entry['test_results_data']))
        print meas_results
        mean_value = numpy.mean(meas_results_calcs)
        print mean_value
        max_value = numpy.amax(meas_results_calcs)
        min_value = numpy.amin(meas_results_calcs)
        median_value = numpy.median(meas_results_calcs)
        std_value = numpy.std(meas_results_calcs)
        report_results = {'company_nickname':company_nickname, 'config_name':config_name, 'mean_value':mean_value, 'max_value':max_value, 'min_value':min_value, 'median_value':median_value, 'std_value':std_value, 'meas_results':meas_results}
        render_json(self, report_results)
        #self.render('report_detail.html', report_results = report_results)




