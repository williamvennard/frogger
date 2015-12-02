from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import ConfigDB
from onedb import ConfigDB_key
from onedb import company_key
from onedb import CommentsDB
from onedb import OscopeDB
from onedb import OscopeDB_key
from onedb import Scope
from onedb import agilentBaseScope
from onedb import agilentBaseInfiniiVision
from onedb import agilent7000
from onedb import agilent7000A
from onedb import agilentMSO7014A
import datetime
import jinja2
import json
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
import appengine_config
from profile import get_profile
from profile import set_profile_cookie
from profile import get_profile_cookie
#from send_script_post import Script

def get_google_user():
    user = None
    try:
       user = oauth.get_current_user('https://www.googleapis.com/auth/userinfo.email')
       logging.info("instruments:get: from oauth.get_current_user: user = %s" % user)
    except:
       pass
    if not user:
       user = users.get_current_user()
    logging.info("get_google_user: user = %s" % user)
    return user

class Handler(InstrumentDataHandler):
    def get(self, author="", instrument_type="", instrument_name=""):
        #if not self.authcheck():
        #    return
        #author = author_creation()
        #name_of_inst = 'myscope'
        #company_name = 'Acme'
        #key = name_of_inst+company_name
        #myscope = agilentMSO7014A(key_name = key)
        user = get_google_user()
        logging.info("instruments:get: user = %s" % user)
        if user:
            active_user = user.email()
            active_user= active_user.split('@')
            author = active_user[0]
            logging.info("instruments:get: author = %s" % author)
        else:
            self.redirect(users.create_login_url(self.request.uri))
        profile = get_profile_cookie(self)
        profile['author'] = author
        if profile['permissions'] == '' or profile['permissions'] == 'viewer':
            self.redirect('/profile')
        instrument_name = instrument_name.split('.')
        if instrument_name[-1] == 'json':
            rows = db.GqlQuery("""SELECT * FROM ConfigDB WHERE author =:1
                                and instrument_type =:2
                                and instrument_name =:3""",
                                author, instrument_type, instrument_name[0])
            inst_config = [r.to_dict() for r in rows]
            rows = db.GqlQuery("""SELECT * FROM OscopeDB WHERE
                                name ='default-scope' ORDER BY TIME ASC""")
            default_data = [r.to_dict() for r in rows]
            inst_default = {"data":default_data, "inst_config":inst_config}
            render_json(self, inst_default)
        elif author and instrument_type and instrument_name:
            rows_inst_details = db.GqlQuery("""SELECT * FROM ConfigDB WHERE
                                             author =:1 and instrument_type
                                             =:2 and instrument_name =:3""",
                                             author, instrument_type,
                                             instrument_name[0])
            self.render('instrument_detail.html', profile=profile)
        else:
            rows = db.GqlQuery("SELECT * FROM ConfigDB WHERE author =:1", author)
            templatedata = {}
            templatedata['info'] = "False"
            self.render('instruments.html', data = templatedata, profile=profile)
            #self.render('instruments.html', data = templatedata, rows = rows)


    def post(self):
        """posts a comment on the test results"""
        user = users.get_current_user()
        if not user.nickname():
            author = "anonymous"
        else:
            author = user.nickname()
        print self.request.body
        profile = get_profile_cookie(self)
        if (not profile) or (profile['permissions'] == 'viewer'):
            self.redirect('/profile')

        data = json.loads(self.request.body)
        config_name = data['config_name']
        trace_name = data['trace_name']
        content = data['content']
        key_name = (config_name + trace_name)
        comment = CommentsDB(key_name = key_name, author=author, content=content, parent=company_key())
        comment.put()
        templatedata = {}
        comment_thread = {}
        comment_thread['content'] = content
        comment_thread['author'] = author
        comment_thread['timestamp'] = timestamp
        templatedata['comment_thread'] = comment_thread
        print templatedata



    # def set_groups_cookie(self, profile):
    #     groups_string = "|".join(profile.groups)
    #     self.response.set_cookie('groups', groups_string)

    # def set_profile_cookies(self, profile):
    #     if hasattr(profile, 'company_nickname'):
    #         self.response.set_cookie('company_nickname',
    #             profile.company_nickname)
    #         self.set_groups_cookie(profile)
    #         return True
    #     else:
    #         return False
