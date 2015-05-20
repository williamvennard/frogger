"""
This is the "data importer" module.  

It takes a http from input and stores it in the database.  It also allows you to display the results of the entry.

"""



import os
import webapp2
import jinja2
import json
import datetime
import re
from time import gmtime, strftime
import collections
import hashlib


from google.appengine.ext import db




template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)


class InstrumentDataHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		return render_str(template, **params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


#def render_post(response, post):
#	response.out.write('<b>' + input.description + '</b><br>')
#	response.out.write(input.inputdata)


def input_key(name = 'default'):
	return db.Key.from_path('inputs', name)


class Input(db.Model):
	description = db.StringProperty(required = True)
	inputdata= db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def render(self):
		self._render_text = self.inputdata.replace('\n', '<br>')
		return render_str("post.html", p = self)

class LinkPage(InstrumentDataHandler):
	def get(self):
		
		datasets = db.GqlQuery("select * from Input order by created desc limit 10")
		jsondata = datasets.get()
		print "you are in the linkpage handler"
		#datasets = jsondata.inputdata
		description = jsondata.description
		
		self.render('data.html', datasets = datasets)


class DataPage(InstrumentDataHandler):
	def get(self):
		
		datasets = db.GqlQuery("select * from Input order by created desc limit 10")
		jsondata = datasets.get()
		#print "you are in the datapage handler"
		#datasets = jsondata.inputdata
		description = jsondata.description
		
		self.render('data.html', datasets = datasets)



class InputPage(InstrumentDataHandler):


    def get(self):
        self.render("front.html")
        print "you are in the get handler"

    def post(self):
		print "you are in the posthandler"
		inputdata = self.request.get("inputdata")
		description = self.request.get("description")
		i = Input(parent = input_key(), inputdata = inputdata, description = description)
		i.put()
		j = str(i.key().id())
		print j
		#self.render("front.html")
		self.redirect('/data')
		

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
	('/input', InputPage),
	('/data/?', DataPage),
	('/data/' + PAGE_RE, LinkPage),
], debug=True)
