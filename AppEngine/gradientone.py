import webapp2
import jinja2
import json
import logging
import os
from onedb import BscopeDB
from onedb import BscopeDB_key
from onedb import OscopeDB
from onedb import OscopeDB_key
from onedb import CapabilitiesDB
from onedb import TestDB
from onedb import TestDB_key
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import oauth
import hashlib
import traceback


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

authorized_users = ['charlie@gradientone.com',
                    'nedwards@gradientone.com',
                    'nickedwards@gmail.com'
#                    'nhannotte@gradientone.com',
#                    'wvennard@gradientone.com',
                    'test@example.com',
                   ]

##
# Question:
# Can we replace this with the jrender_str method in InstrumentDataHandler?
##
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def getKey(row):
    return float(row.DTE)

def getTestKey(tconfigs):
    return tconfigs['date_created']

def getOrderKey(orders):
    return orders['order']

def author_creation():
    "Use the cookie to return the author"
    user = users.get_current_user()
    if user:
        active_user = user.email()
        active_user= active_user.split('@')
        author = active_user[0]
    else:
        self.redirect(users.create_login_url(self.request.uri))
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

def co_and_tp_names(incoming): 
    split_incoming =  incoming.split('&')
    company_list = split_incoming[0].split('=')
    company_nickname = company_list[1]
    testplan_name_list = split_incoming[1].split('=')
    testplan_name = testplan_name_list[1]
    return company_nickname, testplan_name
    

def get_ordered_list(order):
    order = order.split(',')
    middle_section = order[1:-1]
    if len(order) == 1:
        f = order[0]
        f = f.lstrip('[')
        f = f.lstrip('u')
        f = f.rstrip(']')
        f = f.strip('\'')
        f = f.split(':')
        fdict = {}
        fdict['type'] = f[0]
        fdict['name'] = f[1]
        fdict['order'] = f[-1]
        order_list = [fdict]
    else:
        mdict = {}
        for m in middle_section:
            m = m.strip()
            m = m.lstrip('u')
            m = m.strip('\'')
            m = m.split(':')
            mdict['type'] = m[0]
            mdict['name'] = m[1]
            mdict['order'] = m[-1]
        f = order[0]
        f = f.lstrip('[')
        f = f.lstrip('u')
        f = f.strip('\'')
        f = f.split(':')
        fdict = {}
        fdict['type'] = f[0]
        fdict['name'] = f[1]
        fdict['order'] = f[-1]
        l = order[-1]
        l = l.strip()
        l = l.rstrip(']')
        l = l.lstrip('u')
        l = l.strip('\'')
        l = l.split(':')
        ldict = {}
        ldict['type'] = l[0]
        ldict['name'] = l[1]
        ldict['order'] = l[-1]
        order_list = []
        if mdict:
            order_list = [mdict, ldict, fdict]
        else:
            order_list = [ldict, fdict]
    order_list = sorted(order_list, key=getOrderKey)
    return order_list    

def is_checked(self,c,param):
    "Mesurement checked and up date test object 'c'."
    checked = self.request.get(param)
    if checked:
        setattr(c,param,True)
    else:
        setattr(c,param,False)

class InstrumentDataHandler(webapp2.RequestHandler):
    authorized = False
    def write(self, *a, **kw): self.response.out.write(*a, **kw)
    def jrender_str(self, template, **params):
        jtmplt = jinja_env.get_template(template)
        return jtmplt.render(params)
    def render_str(self, template, **params):
        return self.jrender_str(template, **params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def authcheck(self, check_admin=False):
        user = users.get_current_user()
        print user
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
    def canvascookie(self, check_admin = False):
        user = users.get_current_user()
        if user:
            if user.email() in authorized_users:
                utf8username = user.email().encode("utf-8")
                cookie_hash = hashlib.sha1(user.email()).hexdigest()
                print cookie_hash
                self.response.headers.add_header('Set-Cookie', 'user= %s|%s' % (utf8username, cookie_hash))
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


def instruments_and_explanations(analog_bandwidth, analog_sample_rate, capture_buffer_size, capture_channels, resolution):
    inst_list =[]
    c = CapabilitiesDB.all()
    results = c.run(batch_size=1000)
    for r in results:
        inst_list.append(r.instrument_type)
    master_insts =[]
    master_explanations = []
    for i in inst_list:
        qualify_list = []
        exclusion_list = []
        c = CapabilitiesDB.gql("WHERE instrument_type=:1 and analog_bandwidth >=:2", i, int(analog_bandwidth))
        results = c.get()
        if hasattr(results, 'instrument_type'):
            qualify_list.append(results.instrument_type)
        else:
            exclusion_list.append('The Analog Bandwidth you specified does not meet available capabilities')
        c = CapabilitiesDB.gql("WHERE instrument_type=:1 and analog_sample_rate >=:2", i, int(analog_sample_rate))
        results = c.get()
        if hasattr(results, 'instrument_type'):
            qualify_list.append(results.instrument_type)
        else:
            exclusion_list.append('The Analog Sample Rate you specified does not meet available capabilities')
        c = CapabilitiesDB.gql("WHERE instrument_type=:1 and capture_buffer_size >=:2", i, int(capture_buffer_size))
        results = c.get()
        if hasattr(results, 'instrument_type'):
            qualify_list.append(results.instrument_type)
        else:
            exclusion_list.append('The Capture Buffer Size you specified does not meet available capabilities')
        c = CapabilitiesDB.gql("WHERE instrument_type=:1 and capture_channels >=:2", i, int(capture_channels))
        results = c.get()
        if hasattr(results, 'instrument_type'):
            qualify_list.append(results.instrument_type)
        else:
            exclusion_list.append('The number of Capture Channels you specivied does not meet available capabilities')
        c = CapabilitiesDB.gql("WHERE instrument_type=:1 and resolution >=:2", i, int(resolution))
        results = c.get()
        if hasattr(results, 'instrument_type'):
            qualify_list.append(results.instrument_type)
        else:
            exclusion_list.append('The resolution you specified does not meet available capabilities')
        if len(qualify_list) <5:
            master_explanations.append(exclusion_list)
        else:
            qualify_list = set(qualify_list)
            print qualify_list
            for q in qualify_list:
                master_insts.append(q)
    if len(master_insts) >0:
        master_explanations = "This instrument is available."
    else:
        master_insts = "No instruments available."
    return master_insts, master_explanations

def oauth_check(self):
    scope = 'https://www.googleapis.com/auth/userinfo.email'
    # self.response.write('\noauth.get_current_user(%s)' % repr(scope)) # Debug check
    try:
      user = oauth.get_current_user(scope)
      allowed_clients = ['287290951141-dl34gtgp8tvnanm809utk7if4klj0upg.apps.googleusercontent.com'] # list your client ids here
      token_audience = oauth.get_client_id(scope)
      if token_audience not in allowed_clients:
        raise oauth.OAuthRequestError('audience of token \'%s\' is not in allowed list (%s)'
                                      % (token_audience, allowed_clients))

      # Debug statements for verfiying Oauth 2.0
      # self.response.write(' = %s\n' % user)
      # self.response.write('- auth_domain = %s\n' % user.auth_domain())
      # self.response.write('- email       = %s\n' % user.email())
      # self.response.write('- nickname    = %s\n' % user.nickname())
      # self.response.write('- user_id     = %s\n' % user.user_id())
      return True
    except oauth.OAuthRequestError, e:
      self.response.set_status(401)
      self.response.write(' -> %s %s\n' % (e.__class__.__name__, e.message))
      logging.warn(traceback.format_exc())
      return False


class check_testplan_name(InstrumentDataHandler):
    def get(self, testplan_name):
        key = TestDB_key(testplan_name)
        testplan = TestDB.get(key)
        retval = {}
        if testplan:
            retval['available'] = False
        else:
            retval['available'] = True
        render_json(self, retval)
