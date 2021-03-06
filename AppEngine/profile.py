from gradientone import InstrumentDataHandler
from gradientone import query_to_dict
from gradientone import create_psettings
from gradientone import convert_str_to_cha_list
from gradientone import render_json
from gradientone import unic_to_ascii
from gradientone import author_creation
from onedb import UserDB
from onedb import ProfileDB
import collections
import csv
import datetime
import hashlib
import itertools
import jinja2
import json
import logging
import os
import re
import time
import webapp2
import math
from google.appengine.api import memcache
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.ext import db
from time import gmtime, strftime
from collections import OrderedDict
import numpy as np
import appengine_config
import decimate
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from string import maketrans
from datetime import datetime

def get_profile():
    """Get profile object"""
    user = users.get_current_user()
    if user:
        q = ProfileDB.all().filter("email =", user.email())
        profile = q.get()
        print "GET PROFILE CALLED: ", profile
        return profile
    else:
        return None

def login_check(self):
    user = users.get_current_user()
    if user:
        return True
    else:
        self.redirect(users.create_login_url(self.request.uri))

def get_profile_cookie(self):
    """Get cookie data else grabs DB profile and sets cookie. Returns Dictionary."""
    login_check(self)
    comp_cookie = self.request.cookies.get("company_nickname")
    permissions = self.request.cookies.get("permissions")
    name = self.request.cookies.get("name")
    profile = collections.defaultdict(str)
    if comp_cookie and name:
        raw_groups = self.request.cookies.get("groups")
        if raw_groups:
            groups = raw_groups.split("|")
        else:
            groups = []
        profile['groups'] = groups
        profile['company_nickname'] = comp_cookie
        profile['permissions'] = permissions
        profile['name'] = name 
    else:
        fresh_profile = get_profile()
        if fresh_profile:
            profile = fresh_profile
            if  hasattr(profile, 'to_dict'):
                set_profile_cookie(self, profile)
                profile = profile.to_dict()
    return profile

def set_groups_cookie(self, profile):
    groups = profile.groups
    if groups:
        groups_string = "|".join(profile.groups)
    else:
        groups_string = None
    self.response.set_cookie('groups', groups_string)

def set_profile_cookie(self, profile):
    if hasattr(profile, 'company_nickname'):
        self.response.set_cookie('company_nickname',
            profile.company_nickname)
        self.response.set_cookie('permissions', profile.permissions)
        self.response.set_cookie('name', profile.name)
        set_groups_cookie(self, profile)
        return True
    else:
        return False



class Handler(InstrumentDataHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            q = ProfileDB.all().filter("email =", user.email())
            profile = q.get()
            if profile:
                # update user id if needed
                if profile.userid != user.user_id():
                    profile.userid = user.user_id()
                    profile.put()
                set_profile_cookie(self, profile)
                raw_groups = self.request.cookies.get("groups")
                comp_cookie = self.request.cookies.get("company_nickname")
                self.render('profile.html', profile=profile, groups=raw_groups,
                    comp_cookie=comp_cookie)
            else:
                self.render('profile.html', profile="", groups="",
                    error="No profile for this account. Contact your \
                    administrator for help")
        else:
            self.redirect(users.create_login_url(self.request.uri))


def create_profile(self):
        email = self.request.get('email')
        name = self.request.get('name')
        companyname = self.request.get('companyname')
        company_nickname = companyname.strip()
        company_nickname = company_nickname.replace(" ", "_")
        permissions = self.request.get('permissions')
        if permissions == 'admin':
            admin = True
        else:
            admin = False
        profile = ProfileDB(email = email,
                      company_nickname = company_nickname,
                      name = name,
                      permissions = permissions,
                      admin = admin,
                      )
        profile.put()


class AdduserPage(InstrumentDataHandler):
    def get(self):
        profile = get_profile()
        if profile:
            if (profile.admin) or (profile.permissions == 'admin'):
                self.render('adduser.html',
                    company_nickname=profile.company_nickname)
            else:
                self.redirect('/profile')
        else:
            self.redirect('/')

    def post(self):
        create_profile(self)
        self.redirect('/listusers')


class AdminAddUser(InstrumentDataHandler):
    def get(self):
        self.render('admin_adduser.html')
    def post(self):
        create_profile(self)
        self.redirect('/admin/editusers')


class ListUsersPage(InstrumentDataHandler):
    def get(self):
        profile = get_profile()
        if hasattr(profile, 'admin'):
            if (profile.admin) or (profile.permissions == 'admin'):
                company_nickname = profile.company_nickname
                profiles = ProfileDB.all().filter("company_nickname =", company_nickname)
                if profiles:
                    self.render('listusers.html',company=company_nickname,
                                profiles=profiles)
                else:
                    self.render('listusers.html',company="new company?",
                                profiles=profiles)
            else:
                self.redirect('profile')
        else:
            self.redirect('/')


    def post(self):
        email = self.request.get('user_email')
        q = ProfileDB.all().filter("email =", email)
        profile = q.get()

        group = self.request.get('group')
        profile.groups.append(group)
        profile.put()

        group_to_delete = self.request.get('group_to_delete')
        profile.groups.remove(group_to_delete)
        profile.put()
        profile.groups = filter(None, profile.groups)
        profile.put()

        self.redirect('/listusers')


class AdminEditUsers(InstrumentDataHandler):
    """docstring for AdminEditUsers InstrumentDataHandler"""
    def get(self):
        profiles = ProfileDB.all()
        self.render('admin_editusers.html', profiles=profiles)

    def post(self):
        email = self.request.get('user_email')
        q = ProfileDB.all().filter("email =", email)
        profile = q.get()

        group = self.request.get('group')
        profile.groups.append(group)
        profile.put()

        group_to_delete = self.request.get('group_to_delete')
        profile.groups.remove(group_to_delete)
        profile.put()
        profile.groups = filter(None, profile.groups)
        profile.put()

        self.redirect('/admin/editusers')

