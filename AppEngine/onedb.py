from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


def company_key(name = 'default'):
    return db.Key.from_path('companies', name)

def ConfigDB_key(company_nickname ="", config_name =""):
    print 'onedb', config_name
    return db.Key.from_path(company_nickname, config_name)

class ConfigDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    hardware_name = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    config_name = db.StringProperty(required = False)
    sample_rate = db.IntegerProperty(required = False)
    number_of_samples = db.IntegerProperty(required = False)
    commence_test = db.BooleanProperty(required = False)
    commence_explore = db.BooleanProperty(required = False)
    analog_bandwidth = db.StringProperty(required = False)
    test_plan = db.BooleanProperty(required = True)
    trace = db.BooleanProperty(required = True)
    active_testplan_name = db.StringProperty(required = False)
    instrument_status = db.StringProperty(required = False)
    tests = db.ListProperty(db.Key)


def DutDB_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)

class DutDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    author = db.StringProperty(required = True)
    dut_type = db.StringProperty(required = True)
    dut_name = db.StringProperty(required = False)
    settings = db.StringProperty(required = False)
    tests = db.ListProperty(db.Key)

def MeasurementDB_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)

class MeasurementDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    author = db.StringProperty(required = True)
    meas_type = db.StringProperty(required = True)
    meas_name = db.StringProperty(required = False)
    meas_start_time = db.FloatProperty(required = False)
    meas_stop_time = db.FloatProperty(required = False)
    tests = db.ListProperty(db.Key)

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
    #config_name = db.StringProperty(required = False)
    author = db.StringProperty(required = False)
    date_created = db.DateTimeProperty(auto_now_add = True)
    #instrument_type = db.StringProperty(required = False)
    #hardware_name = db.StringProperty(required = False)
    measurement_name = db.StringProperty(required = False)
    sequence_name = db.StringProperty(required = False)
    device_under_test = db.StringProperty(required = False)
    public = db.BooleanProperty(required = False)    
    commence_test = db.BooleanProperty(required = False)
    test_plan = db.BooleanProperty(required = True)
    test_status = db.StringProperty(required = False)
    trace = db.BooleanProperty(required = True)
    configs = db.ListProperty(db.Key)
    start_time = db.DateTimeProperty(required = False)
    duts = db.ListProperty(db.Key)
    measurements = db.ListProperty(db.Key)
    order = db.StringListProperty()
    stop_time = db.DateTimeProperty(required = False)
    test_ready = db.BooleanProperty(required = False)
    test_scheduled = db.BooleanProperty(required = False)
    scheduled_start_time = db.DateTimeProperty(required = False)


class StateDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    version = db.IntegerProperty(required = False)
    widget = db.StringProperty(required = False)
    start_time = db.DateTimeProperty(required = False)
    stop_time = db.DateTimeProperty(required = False)
    error = db.StringProperty(required = False)
    name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    order = db.IntegerProperty(required = False)


def BscopeDB_key(name = 'default'):
    return db.Key.from_path('bscope', name)

class BscopeDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    hardware_name = db.StringProperty(required = True)
    config_name = db.StringProperty(required = True)
    i_settings = db.StringProperty(required = True)
    p_settings = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    cha = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)


def TestResultsDB_key(name = 'default'):
    return db.Key.from_path('testresults', name)

class TestResultsDB(DictModel):
    testplan_name = db.StringProperty(required = False)
    config_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    Total_Slices = db.IntegerProperty(required = False)
    Current_slice_count = db.IntegerProperty(required = False)
    Dec_msec_btw_samples = db.IntegerProperty(required = False)
    Raw_msec_btw_samples = db.IntegerProperty(required = False)
    Slice_Size_msec = db.IntegerProperty(required = False)
    dec_data_url = db.StringProperty(required = False)
    raw_data_url = db.StringProperty(required = False)
    config_name = db.StringProperty(required = False)
    hardware_name = db.StringProperty(required = False)
    start_tse = db.IntegerProperty(required = False)
    test_complete = db.IntegerProperty(required = False)
    test_complete_bool = db.BooleanProperty(required = False)
    trace = db.BooleanProperty(required = False)
    test_plan = db.BooleanProperty(required = False)
    saved_state = db.BooleanProperty(required = False)


class CapabilitiesDB(DictModel):
    instrument_type = db.StringProperty(required = False)
    analog_bandwidth = db.IntegerProperty(required = False)
    capture_channels = db.IntegerProperty(required = False)
    analog_sample_rate = db.IntegerProperty(required = False)
    resolution = db.IntegerProperty(required = False)
    capture_buffer_size = db.IntegerProperty(required = False)

class InstrumentsDB(DictModel):
    capabilities = db.ReferenceProperty(CapabilitiesDB, collection_name = 'instruments')
    instrument_type = db.StringProperty(required = False)
    hardware_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    serial_number = db.StringProperty(required = False)


