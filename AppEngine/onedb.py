from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


def ConfigDB_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)

class ConfigDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    hardware_name = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    instrument_name = db.StringProperty(required = False)
    source = db.StringProperty(required = False)
    horizontal_position = db.FloatProperty(required = False)
    horizontal_seconds_per_div = db.FloatProperty(required = False)
    vertical_position = db.FloatProperty(required = False)
    vertical_volts_per_division = db.FloatProperty(required = False)
    trigger_type = db.StringProperty(required = False)
    frequency_center = db.FloatProperty(required = False)
    frequency_span = db.FloatProperty(required = False)
    frequency_start = db.FloatProperty(required = False)
    frequency_stop = db.FloatProperty(required = False)
    power = db.FloatProperty(required = False)
    sample_rate = db.IntegerProperty(required = False)
    number_of_samples = db.IntegerProperty(required = False)
    commence_test = db.BooleanProperty(required = False)
    test_plan = db.BooleanProperty(required = True)
    testplan_name = db.StringProperty(required = False)
    trace = db.BooleanProperty(required = True)
    instrument_status = db.StringProperty(required = False)

def OscopeDB_key(name = 'default'):
    return db.Key.from_path('oscope', name)

class OscopeDB(DictModel):
    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    data = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)

def TestDB_key(name = 'default'):
    return db.Key.from_path('tests', name)

class TestDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    author = db.StringProperty(required = False)
    date_created = db.DateTimeProperty(auto_now_add = True)
    instrument_type = db.StringProperty(required = False)
    measurement_P2P = db.BooleanProperty(required = False)
    measurement_Peak = db.BooleanProperty(required = False)
    measurement_RMS = db.BooleanProperty(required = False)
    RMS_time_start = db.FloatProperty(required = False)
    RMS_time_stop = db.FloatProperty(required = False)
    measurement_RiseT = db.BooleanProperty(required = False)
    public = db.BooleanProperty(required = False)    
    commence_test = db.BooleanProperty(required = False)
    test_plan = db.BooleanProperty(required = True)
    test_status = db.StringProperty(required = False)
    trace = db.BooleanProperty(required = True)

def BscopeDB_key(name = 'default'):
    return db.Key.from_path('bscope', name)

class BscopeDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    hardware_name = db.StringProperty(required = True)
    instrument_name = db.StringProperty(required = True)
    i_settings = db.StringProperty(required = True)
    p_settings = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    cha = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)

def TestResultsDB_key(name = 'default'):
    return db.Key.from_path('testresults', name)

class TestResultsDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    Total_Slices = db.IntegerProperty(required = False)
    Current_slice_count = db.IntegerProperty(required = False)
    Dec_msec_btw_samples = db.IntegerProperty(required = False)
    Raw_msec_btw_samples = db.IntegerProperty(required = False)
    Slice_Size_msec = db.IntegerProperty(required = False)
    dec_data_url = db.StringProperty(required = False)
    raw_data_url = db.StringProperty(required = False)
    instrument_name = db.StringProperty(required = False)
    hardware_name = db.StringProperty(required = False)
    start_tse = db.IntegerProperty(required = False)
    test_complete = db.IntegerProperty(required = False)
    test_complete_bool = db.BooleanProperty(required = False)
    trace = db.BooleanProperty(required = False)
    test_plan = db.BooleanProperty(required = False)
    saved_state = db.BooleanProperty(required = False)