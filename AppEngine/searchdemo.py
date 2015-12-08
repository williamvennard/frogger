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


    # def post(self):
    #     rows = json.loads(self.request.body)
    #     logging.info(str(rows))
    #     logging.info(rows[1].keys())
        #   #logging.info(dir(search))
        # idx = search.Index(name='powermeterdemo')
        # for row in rows[1:]:
        #     logging.info("max_value = %s" % row['max_value'])
        #     fields = [
        #         search.NumberField(name='max_value',
        #                            value=float(row['max_value'])),
        #         search.NumberField(name='min_value',
        #                            value=float(row['min_value'])),
        #         search.NumberField(name='dB',
        #                            value=float(row['data'])), # 'data' yuck!
        #         search.TextField(name='pass_fail', value=row['pass_fail']),
        #         search.TextField(name='start_time', value=row['Start_TSE']),
        #         search.TextField(name='config_name', value=row['config_name']),
        #         search.NumberField(name='correction_frequency',
        #                            value=float(row['correction_frequency'])),
        #         search.TextField(name='active_testplan_name',
        #                          value=row['active_testplan_name']),
        #     ]
        #     d = search.Document(doc_id=row['Start_TSE'], fields=fields)
        #     try:
        #       add_result = idx.put(d)
        #     except search.Error:
        #       logging.error("search.Index error")
