"""
The new_u2000_post module supplies one class, agilentu2000.

"""


import datetime
import json
import requests
import csv

# import urllib3
# from urllib3.poolmanager import PoolManager
from requests_toolbelt.multipart.encoder import MultipartEncoder

class agilentu2000:
    """Send script config to server.
    >>> u2000dict = ({'Start_TSE':1330181132570, 'data(dBm)':-66.2397506,
                   'i_settings':{'pass_fail_type': u'Range',
                'max_value': u'-40.0', 'min_value': u'-70.0',
                'offset': u'0.0', 'correction_frequency': u'1e9',
                'pass_fail': u'True'}, 'config_name':u'Batchtdoc',
                'active_testplan_name':u'Doctest', 'test_plan':u'False'})
    >>> s = requests.session()
    >>> x = agilentu2000(u2000dict, s)
    >>> x.transmitraw()
    r.reason= OK
    r.status_code= 200
    >>> x.testcomplete()
    c.reason= OK
    c.status_code= 200
    >>> x.transmitblob()
    b.reason= OK
    b.status_code= 200
    """
    global COMPANYNAME
    global HARDWARENAME
    global GAE_INSTANCE
    global USERNAME
    COMPANYNAME = 'Acme'
    HARDWARENAME = 'Tahoe'
    GAE_INSTANCE = 'gradientone-test'
    USERNAME = 'nedwards'

    def dt2ms(self, dtime):
        """Converts date time to miliseconds
        >>> from new_u2000_client import dt2ms
        >>> import datetime
        >>> dtime = datetime.datetime(2015, 12, 8, 18, 11, 44, 320012)
        >>> dt2ms(dtime)
        1449627104320
        """
        return int(dtime.strftime('%s'))*1000 + int(dtime.microsecond/1000)

    def __init__(self, u2000_test_results, ses):
        self.u2000_test_results = u2000_test_results
        self.ses = ses

    def post_creation_data(self, i_settings, stuffing, start_tse,
                          config_name, active_testplan_name, test_plan):
        """ post_creation_data function sends a json object that tells
           the browser where to get data for plotting
        """
        ses = self.ses
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if test_plan == True:
            raw_data_url = ("https://" + GAE_INSTANCE +
                           ".appspot.com/u2000data/"
                           + COMPANYNAME + '/' + HARDWARENAME +'/'
                           + config_name
                           + "/%s" % start_tse)
            url_t = ("https://" + GAE_INSTANCE
                    + ".appspot.com/u2000_testresults/"
                    + COMPANYNAME + '/' + active_testplan_name
                    + '/' + config_name)
            window_u2000 = ({'i_settings':i_settings, 'cha':stuffing,
                           'raw_data_url':raw_data_url, 'start_tse':start_tse,
                           'test_plan':test_plan, 'config_name':config_name,
                           'testplan_name':active_testplan_name,
                           'hardware_name':HARDWARENAME})
            out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
            r = ses.post(url_t, data=out_u2000, headers=headers)
            #print "dir(r)=", dir(r)
            print "result.reason=", result.reason
            print "result.status_code=", result.status_code
        else:
            raw_data_url = ("https://" + GAE_INSTANCE
                           + ".appspot.com/u2000data/"
                           + COMPANYNAME + '/' + HARDWARENAME +'/'
                           + config_name + "/%s" % start_tse)
            url_t = ("https://" + GAE_INSTANCE
                    + ".appspot.com/u2000_traceresults/"
                    + COMPANYNAME + '/' + HARDWARENAME + '/' + config_name)
            window_u2000 = ({'i_settings':i_settings, 'cha':stuffing,
                           'raw_data_url':raw_data_url, 'start_tse':start_tse,
                           'test_plan':test_plan, 'config_name':config_name,
                           'testplan_name':active_testplan_name,
                           'hardware_name':HARDWARENAME})
            out_u2000 = json.dumps(window_u2000, ensure_ascii=True)
            result = ses.post(url_t, data=out_u2000, headers=headers)
            #print "dir(r)=", dir(r)
            print "result.reason=", result.reason
            print "result.status_code=", result.status_code

    def post_complete(self, active_testplan_name, config_name,
                     test_plan, stop_tse, i_settings,
                    start_tse, test_results):
        """post_complete function sends a json object that can
           tells the server the test is complete
        """
        ses = self.ses
        window_complete = ({'active_testplan_name':active_testplan_name,
                           'cha':test_results, 'config_name':config_name,
                           'test_plan':test_plan, 'stop_tse':stop_tse,
                           'i_settings':i_settings, 'start_tse':start_tse,
                           'hardware_name':HARDWARENAME})
        out_complete = json.dumps(window_complete, ensure_ascii=True)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url_c = ("https://" + GAE_INSTANCE +".appspot.com/u2000_testcomplete/"
                + COMPANYNAME + '/' + active_testplan_name
                + '/' +config_name + "/%s" % str(stop_tse))
        result = ses.post(url_c, data=out_complete, headers=headers)
        print "result.reason=", result.reason
        print "result.status_code=", result.status_code
        #print "dir(c)=", dir(c)

    def transmitraw(self):
        """transmitraw function sends a json object that can
           be used for UI presentation
        """
        test_results = self.u2000_test_results['data(dBm)']
        i_settings = self.u2000_test_results['i_settings']
        test_plan = self.u2000_test_results['test_plan']
        config_name = self.u2000_test_results['config_name']
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        start_tse = int(self.u2000_test_results['Start_TSE'])
        self.post_creation_data(i_settings, test_results,
                                start_tse, config_name,
                                active_testplan_name, test_plan)

    def testcomplete(self):
        """transmitcomplete function sends a json object that is used
           to update DB on test status.
        """
        stop_tse = self.dt2ms(datetime.datetime.now())
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        config_name = self.u2000_test_results['config_name']
        test_plan = self.u2000_test_results['test_plan']
        i_settings = self.u2000_test_results['i_settings']
        start_tse = int(self.u2000_test_results['Start_TSE'])
        test_results = self.u2000_test_results['data(dBm)']
        self.post_complete(active_testplan_name, config_name,
                           test_plan, stop_tse, i_settings,
                           start_tse, test_results)

    def transmitblob(self):
        """transmitblob function sends a json object that
          puts the test results in the blobstore
        """
        active_testplan_name = self.u2000_test_results['active_testplan_name']
        config_name = self.u2000_test_results['config_name']
        blob_u2k_tr = self.u2000_test_results.copy()
        blob_u2k_tr['offset(dBm)'] = (blob_u2k_tr['i_settings']['offset'])
        blob_u2k_tr['correction_frequency(Hz)'] = (blob_u2k_tr['i_settings']['correction_frequency'])
        blob_u2k_tr['max_value'] = blob_u2k_tr['i_settings']['max_value']
        blob_u2k_tr['min_value'] = blob_u2k_tr['i_settings']['min_value']
        if float(blob_u2k_tr['min_value']) <= float(blob_u2k_tr['data(dBm)']) <= float(blob_u2k_tr['max_value']):
            blob_u2k_tr['pass_fail'] = 'PASS'
        elif blob_u2k_tr['i_settings']['pass_fail_type'] == 'N/A':
            blob_u2k_tr['pass_fail'] = 'N/A'
        else:
            blob_u2k_tr['pass_fail'] = 'FAIL'
        if blob_u2k_tr['test_plan'] == 'False':
            blob_u2k_tr['measurement_source'] = 'Instrument'
        else:
            blob_u2k_tr['measurement_source'] = 'Testplan'
        blob_u2k_tr['pass_fail_type'] = blob_u2k_tr['i_settings']['pass_fail_type']
        blob_u2k_tr['hardware_name'] = HARDWARENAME
        del blob_u2k_tr['i_settings']
        filename = config_name + ':' + active_testplan_name
        fileblob = open('/home/'
                   + USERNAME + '/' + COMPANYNAME
                   + '/Blobs/tempfile.csv', 'w')
        wblob = csv.writer(fileblob)
        wblob.writerow(blob_u2k_tr.keys())
        wblob.writerow(blob_u2k_tr.values())
        fileblob.close()
        multipartblob = MultipartEncoder(
                   fields={'field0':(filename, open('/home/'
                   + USERNAME + '/' + COMPANYNAME
                   + '/Blobs/tempfile.csv', 'rb'), 'text/plain')}
                   )
        blob_url = requests.get("https://"
                   + GAE_INSTANCE + ".appspot.com/upload/geturl")
        result = requests.post(blob_url.text, data = multipartblob, 
                          headers={'Content-Type': m.content_type})
        print "result.reason=", result.reason
        print "result.status_code=", result.status_code

if __name__ == "__main__":
    import doctest
    doctest.testmod()
