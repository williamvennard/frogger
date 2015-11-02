from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class FlexModel(db.Expando):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

def company_key(name = 'default'):
    return db.Key.from_path('companies', name)

def ConfigDB_key(company_nickname ="", config_name =""):
    print 'onedb', config_name
    return db.Key.from_path('ConfigDB',company_nickname+config_name)

class ConfigDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)
    hardware_name = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    instrument_type = db.StringProperty(required = True)
    config_name = db.StringProperty(required = False)
    analog_sample_rate = db.IntegerProperty(required = False)
    capture_buffer_size = db.IntegerProperty(required = False)
    commence_test = db.BooleanProperty(default = False)
    commence_explore = db.BooleanProperty(required = False)
    analog_bandwidth = db.StringProperty(required = False)
    test_plan = db.BooleanProperty(required = True)
    trace = db.BooleanProperty(required = True)
    active_testplan_name = db.StringProperty(required = False)
    instrument_status = db.StringProperty(required = False)
    capture_channels = db.IntegerProperty(required = False)
    tests = db.ListProperty(db.Key)

class ScriptConfigDB(DictModel):
    name = db.StringProperty(required = True)

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
    config_name = db.StringProperty(required = False)
    author = db.StringProperty(required = False)
    date_created = db.DateTimeProperty(auto_now_add = True)
    #instrument_type = db.StringProperty(required = False)
    hardware_name = db.StringProperty(required = False)
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

class TestInterface(FlexModel):
    name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)

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

class ResultsData(DictModel):
    comment_list = db.ListProperty(db.Key)
        
def BscopeDB_key(company_nickname="", config_name=""):
    return db.Key.from_path('BscopeDB', company_nickname+config_name)

class BscopeDB(ResultsData):
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
    u2000_result = db.StringProperty(required = False)


class CapabilitiesDB(DictModel):
    instrument_type = db.StringProperty(required = False)
    analog_bandwidth = db.IntegerProperty(required = False)
    capture_channels = db.IntegerProperty(required = False)
    analog_sample_rate = db.IntegerProperty(required = False)
    resolution = db.IntegerProperty(required = False)
    capture_buffer_size = db.IntegerProperty(required = False)
    channel_count = db.IntegerProperty(required = False)
    frequency_low = db.StringProperty(required = False)
    frequency_high = db.StringProperty(required = False)
    power_low = db.StringProperty(required = False)
    power_high = db.StringProperty(required = False)
        

class InstrumentsDB(DictModel):
    capabilities = db.ReferenceProperty(CapabilitiesDB, collection_name = 'instruments')
    instrument_type = db.StringProperty(required = False)
    hardware_name = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    serial_number = db.StringProperty(required = False)


def UserDB_key(name = 'default'):
    return db.Key.from_path('emails', name)

class UserDB(DictModel):
    company_nickname = db.StringProperty(required = False)
    email = db.StringProperty(required = False)
    admin = db.BooleanProperty(required = False)

def CompanyDB_key(name = 'default'):
    return db.Key.from_path('emails', name)

class ProfileDB(DictModel):
    bio = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False)
    email = db.StringProperty(required = False)
    admin = db.BooleanProperty(required = False)
    name = db.StringProperty(required = False)
    groups = db.StringListProperty()
    userid = db.StringProperty(required = False)

class CompanyDB(DictModel):
    company_nickname = db.StringProperty(required = True)
    users = db.ListProperty(db.Key)
    groups = db.StringListProperty()

class CommunityPostDB(DictModel):
    title           = db.StringProperty(required = True)
    author          = db.StringProperty(required = True)
    date_created    = db.DateTimeProperty(auto_now_add = True)    
    test_ref        = db.ReferenceProperty(TestDB, collection_name = 'community_posts')
    privacy         = db.StringProperty(required = False)
    company_nickname = db.StringProperty(required = False) # company of user posting

class CommentsDB(DictModel):
    author = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    test = db.ReferenceProperty(TestDB, collection_name = 'comments')
    timestamp = db.DateTimeProperty(auto_now_add = True)


class Scope(DictModel):
    acquisition_start_time = db.StringProperty(required = False)
    acquisition_type = db.StringProperty(required = False)
    acquisition_number_of_points_minimum = db.StringProperty(required = False)
    acquisition_record_length = db.StringProperty(required = False)
    acquisition_time_per_record = db.StringProperty(required = False)
    channel_name = db.StringProperty(required = False)
    channel_enabled = db.BooleanProperty(required = False)
    channel_input_impedance = db.StringProperty(required = False)
    channel_input_frequency_max = db.StringProperty(required = False)
    channel_probe_attenuation = db.StringProperty(required = False)
    channel_coupling = db.StringProperty(required = False)
    channel_offset = db.StringProperty(required = False)
    channel_range = db.StringProperty(required = False)
    channel_count = db.StringProperty(required = False)
    measurement_status = db.StringProperty(required = False)
    trigger_coupling = db.StringProperty(required = False)
    trigger_holdoff = db.StringProperty(required = False)
    trigger_level = db.StringProperty(required = False)
    trigger_edge_slope = db.StringProperty(required = False)
    trigger_source = db.StringProperty(required = False)
    trigger_type = db.StringProperty(required = False)


class agilentBaseScope(Scope):
    channel_label = db.StringProperty(required = False)
    channel_probe_skew = db.StringProperty(required = False)
    channel_scale = db.StringProperty(required = False)
    channel_invert = db.StringProperty(required = False)
    channel_probe_id = db.StringProperty(required = False)
    channel_bw_limit = db.StringProperty(required = False)    
    self_test_delay = db.StringProperty(default = '40.0')
    memory_size = db.StringProperty(default = '10.0')
    acquisition_segmented_count = db.StringProperty(default = '2.0')
    acquisition_segmented_index = db.StringProperty(default = '1.0')
    timebase_mode = db.StringProperty(default = 'main')
    timebase_reference = db.StringProperty(default = 'center')
    timebase_position = db.StringProperty(default = '0.0')
    timebase_range = db.StringProperty(default = '1e-3')
    timebase_scale = db.StringProperty(default = '100e-6')
    timebase_window_position = db.StringProperty(default = '0.0')
    timebase_window_range = db.StringProperty(default = '5e-6')
    timebase_window_scale = db.StringProperty(default = '500e-9')
    #display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
    display_vectors = db.StringProperty(default = 'True')
    display_labels = db.StringProperty(default = 'True')


class agilentBaseInfiniiVision(agilentBaseScope):
    pass

        
class agilent7000(agilentBaseInfiniiVision):
    horizontal_divisions = 10
    vertical_divisions = 8

class agilent7000A(agilent7000):
    pass    


class agilentMSO7014A(agilent7000A):
    analog_channel_name = db.StringProperty(required = False)
    analog_channel_count = db.StringProperty(default = '4')
    digital_channel_name = db.StringProperty(required = False)
    digital_channel_count = db.StringProperty(default = '0')
    #channel_count = analog_channel_count + digital_channel_count
    bandwidth = db.StringProperty(default = '100e6')
    horizontal_divisions = db.StringProperty(default = '10')
    vertical_divisions = db.StringProperty(default = '8')


class pwrmeter(DictModel):
    company_nickname = db.StringProperty(required = False) 
    config_name = db.StringProperty(default = 'channel1')  
    channel_range_lower = db.StringProperty(default = '0.0')
    channel_range_upper = db.StringProperty(default = '0.0')
    range_auto = db.StringProperty(default = 'True')
    trigger_source = db.StringProperty(default = 'IMM')  #possible values: BUS, INTernal[1], EXTernal, HOLD, IMMediate
    trigger_internal_event_source = db.StringProperty(default = '')
    trigger_internal_level = db.StringProperty(default = '0.0')
    trigger_internal_slope = db.StringProperty(default = 'positive')
    send_software_trigger = db.StringProperty(default = '')
    duty_cycle_enabled  = db.StringProperty(default = 'True') 
    duty_cycle_value = db.StringProperty(default = '50.0')
    averaging_count   = db.StringProperty(default = 'tbd')
    zero_state= db.StringProperty(default = '')
    zero = db.StringProperty(default = '')
    calibration_state = db.StringProperty(default = '')
    reference_oscillator_enabled = db.StringProperty(default = 'False') 
    reference_oscillator_frequency = db.StringProperty(default = '10e6')
    reference_oscillator_level = db.StringProperty(default = '0.0')

def agilentU2000_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)
    
class agilentU2000(pwrmeter):
    channel_count = db.StringProperty(default = '1')
    averaging_count_auto = db.StringProperty(default = 'True')
    correction_frequency = db.StringProperty(default = '50e6')
    offset = db.StringProperty(default = '0.0')
    units = db.StringProperty(default = 'dBm')
    pass_fail = db.StringProperty(default = False)
    pass_fail_type = db.StringProperty(default = "")
    max_value = db.StringProperty(default = '0.0')
    min_value = db.StringProperty(default = '0.0')

def agilentU2000data_key(name = 'default'):
    return db.Key.from_path('company_nickname', name)

class agilentU2000data(ResultsData):
    company_nickname = db.StringProperty(required = True)
    hardware_name = db.StringProperty(required = True)
    config_name = db.StringProperty(required = True)
    i_settings = db.StringProperty(required = True)
    test_results_data = db.TextProperty(required = True)
    start_tse = db.IntegerProperty(required = True)


