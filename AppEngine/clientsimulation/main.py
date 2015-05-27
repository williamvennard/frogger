import webapp2
import requests

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

        r=requests.post("https://accounts.google.com/o/oauth2/token")
#                           headers={
#                               'content-type':'application/x-www-form-urlencoded'},
#                           data={
#                   		    'client_id':'1023941599436-v1mlfpv9ukdv8lfnhkp4snp10f6rc537.apps.googleusercontent.com',
#                               'client_secret':'wiLNYGbRIMRKOq_v_OM0yjN3',
#                               'redirect_uri':'http://localhost/etc'})



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)