import logging
import json
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import search
class Handler(webapp2.RequestHandler):
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
        for index in search.get_indexes(fetch_schema=True):
            logging.info("index %s", index.name)
            logging.info("schema: %s", index.schema)
