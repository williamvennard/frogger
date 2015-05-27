import webapp2
import requests

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

        r=requests.post("https://accounts.google.com/o/oauth2/token")
#                           headers={
#                               'content-type':'application/x-www-form-urlencoded'},
#                           data={
#                   		    'client_id':'1023941599436-s58bk24id29kjbkpa1abn4l82ub2n3bk.apps.googleusercontent.com',
#                               'client_secret':'2Wy0xFTfdvaJ6pg2xqaarNmS',
#                               'redirect_uri':'http://localhost/etc'})



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)