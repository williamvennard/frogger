import datetime
import logging
import json
from cgi import parse_qs
import urllib
from urlparse import urlparse
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import search

from profile import get_profile_cookie
from gradientone import InstrumentDataHandler
from onedb import ProfileDB

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
         rows = json.loads(self.request.body)
         logging.info(str(rows))
         logging.info(rows[1].keys())
           #logging.info(dir(search))
         idx = search.Index(name='powermeterdemo')
         for row in rows[1:]:
             logging.info("max_value = %s" % row['max_value'])
             fields = [
                 search.NumberField(name='max_value',
                                    value=float(row['max_value'])),
                 search.NumberField(name='min_value',
                                    value=float(row['min_value'])),
                 search.NumberField(name='dB',
                                    value=float(row['data'])), # 'data' yuck!
                 search.TextField(name='pass_fail', value=row['pass_fail']),
                 search.TextField(name='start_time', value=row['Start_TSE']),
                 search.TextField(name='config_name', value=row['config_name']),
                 search.NumberField(name='correction_frequency',
                                    value=float(row['correction_frequency'])),
                 search.TextField(name='active_testplan_name',
                                  value=row['active_testplan_name']),
             ]
             d = search.Document(doc_id=row['Start_TSE'], fields=fields)
             try:
               add_result = idx.put(d)
             except search.Error:
               logging.error("search.Index error")

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

class FakeProfile:
    company_nickname = "charliedemos"

class HandlerCharlie(InstrumentDataHandler):
    def get(self):
        uri = urlparse(self.request.uri)
        query = ''
        if uri.query:
            query = parse_qs(uri.query)
            query = query['query'][0]

        # sort results by author descending
        expr_list = [search.SortExpression(
            expression='author', default_value='',
            direction=search.SortExpression.DESCENDING)]
        # construct the sort options
        sort_opts = search.SortOptions(
             expressions=expr_list)
        query_options = search.QueryOptions(
            limit=30,
            sort_options=sort_opts)
        query_obj = search.Query(query_string=query, options=query_options)
        results = search.Index(name='powermeterdemo').search(query=query_obj)
        self.render('searchdemo_charlie.html', results=results, 
            profile=FakeProfile(), query=query,
            number_returned=len(results.results))

    def post(self):
        """Handles a post request."""
        query = self.request.get('search')
        if query:
            self.redirect('/searchdemo/charlie?' + urllib.urlencode(
                #{'query': query}))
                {'query': query.encode('utf-8')}))
        else:
            self.redirect('/searchdemo/charlie/')
