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
from google.appengine.api.search import search as gaesearch
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


class DocHandler(InstrumentDataHandler):
    def post(self):
        profile = get_profile_cookie(self)
        doc_limit = 10
        doc_ids = self.request.params.getall('doc_ids')
        try:
          index = search.Index(settings.INDEX_NAME)
          result_docs = collections.defaultdict()
          for doc_id in doc_ids:
            result_docs[doc_id] = index.get(doc_id).fields
        except search.Error:
          logging.error("Search Results Error: %s" % e )
        name_time = str(dt2ms(datetime.now()))
        newname = profile['name'] + name_time
        key = newname
        memcache.set(key, result_docs)
        self.render('blob_analyzer.html', results = result_docs, 
            download_key = newname, profile = profile)

    def re(self):
        query = self.request.get('search')
        if query:
            self.redirect('/searchdemo?' + urllib.urlencode(
                #{'query': query}))
                {'query': query.encode('utf-8')}))
        else:
            self.redirect('/searchdemo')

# Note max_value == "N/A" will be gaesearch.MAX_NUMBER_VALUE
# Note min_value == "N/A" will be  gaesearch.MIN_NUMBER_VALUE
# Number Field: A double precision floating point value
# between -2,147,483,647 and 2,147,483,647.
# see: https://cloud.google.com/appengine/docs/python/search/

class UploadHandler(InstrumentDataHandler):
    def make_fields(self, row):
        if 'start_time' in row.keys():
            timekey = row['start_time']
            if row['max_value'] == 'N/A':
               max_value = gaesearch.MAX_NUMBER_VALUE
            else:
               max_value = float(row['max_value'])
            if max_value > gaesearch.MAX_NUMBER_VALUE:
               logging.error("%s: max_value=%s too high" % (timekey, max_value))
               max_value = gaesearch.MAX_NUMBER_VALUE - 1
            if row['min_value'] == 'N/A':
               min_value = gaesearch.MIN_NUMBER_VALUE
            else:
               min_value = float(row['min_value'])
            if min_value < gaesearch.MIN_NUMBER_VALUE:
               logging.error("%s: min_value=%s too low" % (timekey, min_value))
               min_value = gaesearch.MIN_NUMBER_VALUE + 1
            correction_frequency = float(row['correction_frequency(Hz)'])
            correction_frequency /= 10000000 # convert to MHz
            if correction_frequency > gaesearch.MAX_NUMBER_VALUE:
               logging.error(
                 "%s: correction_frequencey=%s too high" % (timekey, min_value))
               correction_frequency = gaesearch.MAX_NUMBER_VALUE - 1
            fields = [
                search.NumberField(name='dBm',
                                   value=float(row['data(dBm)'])),
                search.NumberField(name='offset_dBm',
                                   value=float(row['offset(dBm)'])),
                search.NumberField(name='max_value', value=max_value),
                search.NumberField(name='min_value', value=min_value),
                search.TextField(name='pass_fail', value=row['pass_fail']),
                search.DateField(name='start_time', 
                                 value=datetime.fromtimestamp(
                                               int(row['start_time'])//1000)),
                search.TextField(name='msbased_key', value=row['start_time']),
                search.TextField(name='config_name', value=row['config_name']),
                search.TextField(name='measurement_source', 
                                 value=row['measurement_source']),
                search.TextField(name='hardware_name', 
                                 value=row['hardware_name']),
                search.NumberField(name='correction_frequency',
                                   value=correction_frequency),
                search.TextField(name='active_testplan_name',
                                 value=row['active_testplan_name']),
            ]
        else:
            fields = [
                search.NumberField(name='max_value', value=max_value),
                search.NumberField(name='min_value', value=min_value),
                search.NumberField(name='dBm',
                                   value=float(row['data'])), # 'data' yuck!
                search.TextField(name='pass_fail', value=row['pass_fail']),
                search.DateField(name='start_time', 
                                 value=datetime.fromtimestamp(
                                          int(row['start_time'])//1000)),
                search.TextField(name='msbased_key',
                                 value=row['start_time']),
                search.TextField(name='config_name', value=row['config_name']),
                search.NumberField(name='correction_frequency',
                                   value=float(row['correction_frequency'])),
                search.TextField(name='active_testplan_name',
                                 value=row['active_testplan_name']),
            ]
        return fields

    def post(self):
        rows = json.loads(self.request.body)
        #logging.info(str(rows))
        logging.info("rows[0].keys=%s" % rows[0].keys())
        #logging.info(dir(search))
        if 'start_time' in rows[0].keys():
            idx = search.Index(name='powermeterdemo')
            timekey = 'start_time'
        else:
            idx = search.Index(name='oldpowermeterdemo')
            timekey = 'Start_TSE'
        for row in rows[1:]:
            logging.info("max_value = %s" % row['max_value'])
            fields= self.make_fields(row)
            d = search.Document(doc_id=row[timekey], fields=fields)
            try:
              add_result = idx.put(d)
            except search.Error:
              logging.error("search.Index error")

    def get(self):
        self.delete_all()
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

class Results:
    number_found = 0

class Result:
    fields = []

class ResultField:
    name = ''
    value = ''

class HandlerCharlie(InstrumentDataHandler):

    def insert_NA(self,results):

        #NA_strings = [str(gaesearch.MAX_NUMBER_VALUE) + '.0',
        #              str(gaesearch.MIN_NUMBER_VALUE) + '.0']
        #logging.info("NA_strings=%s" % NA_strings)
        NA_values = [float(gaesearch.MAX_NUMBER_VALUE), gaesearch.MIN_NUMBER_VALUE]
        logging.info("NA_values=%s" % NA_values)
        new_results = []
        for result in results:
            new_result = Result()
            new_result.fields = []
            for f in result.fields:
                nf = ResultField()
                nf.value = f.value
                nf.name = f.name
                if 'max' in f.name or 'min' in f.name:
                    logging.info("f=%s" % f)
                    logging.info("f.value=%s" % f.value)
                    logging.info("NA_values[0]=%s" % NA_values[0])
                    if f.value in NA_values:
                        logging.info("changing value to N/A")
                        nf.value = 'N/A'
                new_result.fields.append(nf)
            new_results.append(new_result)
        return new_results

    def get(self):
        uri = urlparse(self.request.uri)
        query = ''
        if uri.query:
            query = parse_qs(uri.query)
            query = query['query'][0]

        # sort results by timestamp descending
        expr_list = [search.SortExpression(
            expression='start_time', default_value='',
            direction=search.SortExpression.DESCENDING)]
        # construct the sort options
        sort_opts = search.SortOptions(
             expressions=expr_list)
        query_options = search.QueryOptions(
            limit=30,
            sort_options=sort_opts)
        query_obj = search.Query(query_string=query, options=query_options)
        results = search.Index(name='powermeterdemo').search(query=query_obj)
        #new_results = results
        new_results = self.insert_NA(results)
        self.render('searchdemo_charlie.html', results=new_results, 
            profile=FakeProfile(), query=query,
            number_found=results.number_found,
            number_returned=len(new_results))

    def post(self):
        """Handles a post request."""
        query = self.request.get('search')
        if query:
            self.redirect('/searchdemo/charlie?' + urllib.urlencode(
                #{'query': query}))
                {'query': query.encode('utf-8')}))
        else:
            self.redirect('/searchdemo/charlie/')

def delete_all_in_index(index_name):
    """Delete all the docs in the given index. Only use when resetting."""
    doc_index = search.Index(name=index_name)

    # looping because get_range by default returns up to 100 documents at a time
    while True:
        # Get a list of documents populating only the doc_id field and extract the ids.
        document_ids = [document.doc_id
                        for document in doc_index.get_range(ids_only=True)]
        if not document_ids:
            break
        # Delete the documents for the given ids from the Index.
        doc_index.delete(document_ids)
