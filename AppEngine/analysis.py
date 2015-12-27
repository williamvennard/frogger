from datetime import datetime
import logging
import json
from cgi import parse_qs
import urllib
from urlparse import urlparse
import webapp2
import collections
import StringIO
import csv
import settings
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import search
from profile import get_profile_cookie
from gradientone import InstrumentDataHandler
from onedb import ProfileDB


def dt2ms(t):
    return str(t.strftime('%s'))*1000 + str(t.microsecond/1000)

class Handler(InstrumentDataHandler):
    def post(self):
        profile = get_profile_cookie(self)
        querystring = self.request.get('query')
        doc_limit = 10
        doc_ids = self.request.get('doc_ids')

        logging.debug("QUERYSTRING: %s" % querystring)

        name_time = str(dt2ms(datetime.now()))
        # sort results by starttime descending
        expr_list = [search.SortExpression(
            expression='start_tse', default_value=name_time,
            direction=search.SortExpression.DESCENDING)]
        # construct the sort options
        sort_opts = search.SortOptions(
            expressions=expr_list)

        try:
          index = search.Index(settings.INDEX_NAME)
          search_query = search.Query(
              query_string=querystring,
              options=search.QueryOptions(
                  limit=doc_limit,
                  sort_options = sort_opts,
              )
          )
          search_results = index.search(search_query)
        except search.Error, e:
          logging.error("Search Query Error: %s" % e )

        try:
          returned_count = len(search_results.results)
          number_found = search_results.number_found
          result_docs = collections.defaultdict()
          for doc in search_results:
            result_docs[doc.doc_id] = doc.fields
            
        except search.Error:
          logging.error("Search Results Error: %s" % e )

        # name_time = str(dt2ms(datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        memcache.set(key, result_docs)
        # logging.debug('QUERY RESULT: %s' % result_docs)
        self.render('blob_analyzer.html', results = result_docs, 
            download_key = newname, profile = profile)

    def get(self):
        for index in search.get_indexes(fetch_schema=True):
            logging.info("index %s", index.name)
            logging.info("schema: %s", index.schema)
        
        profile = get_profile_cookie(self)
        querystring = ""
        doc_limit = 20
        logging.debug("QUERYSTRING: %s" % querystring)
        try:
          index = search.Index(settings.INDEX_NAME)
          search_query = search.Query(
              query_string=querystring,
              options=search.QueryOptions(
                  limit=doc_limit))
          search_results = index.search(search_query)
        except search.Error, e:
          logging.error("Search Query Error: %s" % e )

        try:
          returned_count = len(search_results.results)
          number_found = search_results.number_found
          result_docs = collections.defaultdict()
          # logging.debug("SEARCH: %s" % search_results)
          for doc in search_results:
            result_docs[doc.doc_id] = doc.fields
            
        except search.Error:
          logging.error("Search Results Error: %s" % e )
        name_time = str(dt2ms(datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        memcache.set(key, result_docs)
        self.render('blob_analyzer.html', results = result_docs, 
            download_key = newname, profile = profile)


class DocExport(InstrumentDataHandler):
    def post(self):
        key = self.request.get('download_key')
        result_docs = memcache.get(key)
        headers = self.response.headers
        headers['Content-Type'] = 'text/csv'
        headers['Content-Disposition'] =  ('attachment; filename=export' + 
          str(datetime.now()) + '.csv')
        tmp = StringIO.StringIO()
        writer = csv.writer(tmp)
        counter = 0
        for k,fields in result_docs.iteritems():
            if counter == 0:
                writer.writerow([field.name for field in fields])
                writer.writerow([field.value for field in fields])
            else:
                writer.writerow([field.value for field in fields]) 
            counter +=1
        contents = tmp.getvalue()
        tmp.close()
        self.response.out.write(contents)