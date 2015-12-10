from gradientone import InstrumentDataHandler
import logging
import json
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.api import memcache
from profile import get_profile_cookie
import datetime

INDEX_NAME = 'U2000'

def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

class Handler(InstrumentDataHandler):
    def post(self):
        profile = get_profile_cookie(self)
        querystring = self.request.get('query')
        doc_limit = 10
        logging.debug("QUERYSTRING: %s" % querystring)
        try:
          index = search.Index(INDEX_NAME)
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
          output = []
          logging.debug("SEARCH: %s" % search_results)
          for doc in search_results:
            doc_id = doc.doc_id
            fields = doc.fields
            logging.debug("FIELDS: %s" % fields)
            output.append(fields)
            
        except search.Error:
          logging.error("Search Results Error: %s" % e )

        name_time = str(dt2ms(datetime.datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        # memcache.set(key, output)
        logging.debug('QUERY RESULT: %s' % output)
        self.render('blob_analyzer.html', result = output, 
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
          index = search.Index(INDEX_NAME)
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
          output = []
          logging.debug("SEARCH: %s" % search_results)
          for doc in search_results:
            doc_id = doc.doc_id
            fields = doc.fields
            logging.debug("FIELDS: %s" % fields)
            output.append(fields)
            
        except search.Error:
          logging.error("Search Results Error: %s" % e )
        name_time = str(dt2ms(datetime.datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        self.render('blob_analyzer.html', result = output, 
            download_key = newname, profile = profile)


class UploadHandler(InstrumentDataHandler):
    def post(self):
        profile = get_profile_cookie(self)
        querystring = self.request.get('query')
        doc_limit = 10
        logging.debug("QUERYSTRING: %s" % querystring)
        try:
          index = search.Index(INDEX_NAME)
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
          output = []
          logging.debug("SEARCH: %s" % search_results)
          for doc in search_results:
            doc_id = doc.doc_id
            fields = doc.fields
            logging.debug("FIELDS: %s" % fields)
            output.append(fields)
            
        except search.Error:
          logging.error("Search Results Error: %s" % e )

        name_time = str(dt2ms(datetime.datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        # memcache.set(key, output)
        logging.debug('QUERY RESULT: %s' % output)
        self.render('blob_analyzer.html', result = output, 
            download_key = newname, profile = profile)

    def get(self):
        #self.delete_all()
        if False:
          for index in search.get_indexes(fetch_schema=True):
            logging.info("index attributes: %s", dir(index))
            logging.info("index.delete.__doc__: %s", index.delete.__doc__)
            logging.info("index.get.__doc__: %s", index.get.__doc__)
            logging.info("index.search.__doc__: %s", index.search.__doc__)
        for index in search.get_indexes():
            results = index.search("")
            doc_ids = [ result.doc_id for result in results ]
            logging.info("doc_ids: %s", doc_ids)

    def delete_all(self):
            for index in search.get_indexes():
                results = index.search("")
                doc_ids = [ result.doc_id for result in results ]
                try:
                    index.delete(doc_ids)
                except search.Error, e:
                    logging.error("Search delete index error, e = %s" % str(e))
