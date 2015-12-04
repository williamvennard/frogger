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
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
from google.appengine.api import mail
#from send_script_post import Script

DOMAIN = "gradientone-dev2.appspot.com"

class Handler(InstrumentDataHandler):
    def get(self, company_nickname=""):
        rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE company_nickname =:1", company_nickname)
        a = query_to_dict(rows)
        self.render('report_summary.html', rows = rows)
    def post(self, company_nickname=""):
        recipient_email = self.request.get('recipient_email')
        start_tse = self.request.get('start_tse')
        testplan_name = self.request.get('testplan_name')
        result_url = ('https://' + DOMAIN + '/testlibrary/testresults/' +
            company_nickname + '/' + testplan_name + '/' + start_tse)
        message = mail.EmailMessage(
            sender="GradientOne Support <nedwards@gradientone.com>",
            subject="Test Data For You!")
        message.to = recipient_email
        message.body = """

        John Doe has shared this link with you!

        """ + result_url + """

        GradientOne Inc
        """

        message.send()

