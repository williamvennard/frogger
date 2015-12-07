import json
import os
import requests
from oauth2client.file import Storage
from oauth2client.client import AccessTokenCredentials
import cPickle as pickle

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Until SSL turned on
COMPANYNAME = 'Acme'
HARDWARENAME = 'Tahoe'


def limited_input():
    """To get an initial access token and refresh token"""
    client_id = "287290951141-dl34gtgp8tvnanm809utk7if4klj0upg.apps.googleusercontent.com"
    client_secret = "V5ihqrK506ISAzYFH7V9SRfR"
    r = requests.post("https://www.googleapis.com/oauth2/v3/token",
      data = {"client_id":client_id, "client_secret":client_secret,
              "code":"RSWX-EWPH4/yimM4V0QTSL1ZP95nPe4Q_DpFWcZbHv7xbukFfnjB3w",
              "grant_type":"http://oauth.net/grant_type/device/1.0"})
    print(r.text)


def refresh():
    """Uses refresh token to get new token. Pickles and returns credentials"""
    client_id = "287290951141-dl34gtgp8tvnanm809utk7if4klj0upg.apps.googleusercontent.com"
    client_secret = "V5ihqrK506ISAzYFH7V9SRfR"
    r = requests.post("https://www.googleapis.com/oauth2/v3/token",
    data = {"client_id":client_id, "client_secret":client_secret,
              "refresh_token":"1/HCZswI4mR3ibVUirYLtQXlIgRlU2RYEbTP8p1kFIwkFIgOrJDtdun6zK6XiATCKT",
              "grant_type":"refresh_token"})
    print(r.text)
    raw_cred = r.text
    json_cred = json.loads(r.text)
    pickle.dump(raw_cred, open('saved_cred.p', 'wb'))
    # cred = AccessTokenCredentials(json_cred['access_token'], 'SD-NUC/1.0') # For use with google storage library
    return raw_cred


def get_new_token():
    cred = refresh()
    token = cred['access_token']
    return token


def get_access_token():
    raw_cred = pickle.load(open('saved_cred.p', 'rb'))
    cred = json.loads(raw_cred)
    access_token = cred['access_token']
    return access_token


def check_token(token):
    """Checks token. Returns true if valid. Attemps one refresh if token expired"""
    config_url = "https://gradientone-test.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    r = s.get(config_url, headers=headers)
    if r.status_code == 200:
      return True
    elif r.status_code == 401:
      new_cred = refresh()
      return check_new_token(new_cred)
    else:
      return False


def check_new_token(cred):
    """Checks new token. No refresh"""
    config_url = "https://gradientone-test.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    r = s.get(config_url, headers=headers)
    if r.status_code == 200:
      return True
    else:
      return False


def raw_auth_check():
    """Makes a get request to testplansummary to test functions and tokens"""
    config_url = "https://gradientone-test.appspot.com/testplansummary/" + COMPANYNAME + '/' + HARDWARENAME
    raw_cred = pickle.load(open('saved_cred.p', 'rb'))
    cred = json.loads(raw_cred)
    access_token = cred['access_token']
    headers = {'Authorization': 'Bearer '+access_token}
    #r = requests.get(config_url, headers=headers)
    s = requests.session()
    r = s.get(config_url, headers=headers)
    if r.status_code == 401:
      print 'refresh'
      raw_cred = refresh()
      cred = json.loads(raw_cred)
      access_token = cred['access_token']
      headers = {'Authorization': 'Bearer '+access_token}
      # r = requests.get(config_url, headers=headers)
      r = s.get(config_url, headers=headers)
    print(r.status_code)
    print(r.text)