from gradientone import InstrumentDataHandler
import collections
import webapp2
from google.appengine.api import oauth
from google.appengine.api import users
import appengine_config


class Handler(InstrumentDataHandler):
    def get(self):  
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))