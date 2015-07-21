import webapp2
import jinja2
import json
import logging
import os
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def getKey(row):
    return float(row.DTE)

def getTestKey(tconfigs):
    return tconfigs['date_created']

def author_creation():
    "Use the cookie to return the author"
    user = users.get_current_user()
    if user:
        active_user = user.email()
        active_user= active_user.split('@')
        author = active_user[0]
    return author

def dropdown_creation():
    key = 'instrumentsDB' 
    dropdown = memcache.get(key)
    if dropdown == None:
        logging.error("BscopeData:get: query")
        b = db.GqlQuery("""SELECT * FROM BscopeDB LIMIT 1""")
        o = db.GqlQuery("""SELECT * FROM OscopeDB LIMIT 1""")
        rows_b = list(b)
        rows_o = list(o)
        results_b = query_to_dict(rows_b)
        results_o = query_to_dict(rows_o)
        dropdown = []
        if results_b != []: 
            dropdown.append('BitScope')
        if results_o != []:
            dropdown.append('Tektronix')
        memcache.set(key, dropdown)
    return dropdown

def render_json(self, j):
    json_txt = json.dumps(j)
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.write(json_txt)

def render_json_cached(self,j):
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.write(j)

def query_to_dict(result):
    query_dict = [r.to_dict() for r in result]
    return query_dict

def convert_str_to_cha_list(string):
    bracket_free_data = string[1:-1]
    cha_list = bracket_free_data.split(',')
    cha_list =  [float(x) for x in cha_list]
    return cha_list

def create_psettings(data):
    #data = str(data[0]['config'])
    data = data.split(',')
    temp_list = []
    for d in data[:5]:
        temp_list.append(d)
    temp_dict = {}
    for item in temp_list[1:-1]:
        item = item.split(':')
        temp_dict[item[0].strip().strip('u').strip('\'')] = int((item[1]).strip().rstrip("'").lstrip("'"))
    t = temp_list[0]
    t = t.split(':')
    #del t[0]
    temp_dict[t[0].strip().strip('{').strip('u').strip('\'')] = int((t[1].strip()))
    t = temp_list[-1]
    t = t.split(':')
    temp_dict[t[0].strip().strip('u').strip('\'')] = int((t[1].strip().strip('}')))
    return temp_dict

def unic_to_ascii(input_uni):
    new = {}
    for i in input_uni:
        k = i.encode('ascii')
        if type(input_uni[i]) == unicode:
            v = input_uni[i].encode('ascii')
        else:
            v = input_uni[i]
        new[k] = v
    return new

class InstrumentDataHandler(webapp2.RequestHandler):
    authorized = False
    def write(self, *a, **kw): self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        return render_str(template, **params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def authcheck(self, check_admin=False):
        user = users.get_current_user()
        if user:
            if user.email() in authorized_users:
                return True
            # todo: put in try block and handle exception
            cursor = db.GqlQuery("""SELECT * FROM UserDB 
                                  WHERE email = :1""", 
                                 user.email())
            result = cursor.get()
            if result:
                if user.email() == result.email:
                    if check_admin:
                        if result.admin:
                            authorized = True
                        else:
                            authorized = False
                    else:
                        authorized = True
            else:
                authorized = False
        else:
            authorized = False
        if not authorized:
            self.redirect('/static/autherror.html')
        return authorized