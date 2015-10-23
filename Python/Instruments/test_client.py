import json
import requests
import grequests
import time   # time is a module here
import math
import datetime
import threading
from u2000_post import agilentu2000
import numpy as np
import numpy.fft as fft
import scipy.signal 
import ivi

pm = ivi.agilent.agilentU2001A("USB::0x0957::0x2b18::INSTR")
print 'old pm inititalized should be true', pm.initialized
pm.close()
print 'old pm not initialized should be false', pm.initialized
new_pm = ivi.agilent.agilentU2001A("USB::0x0957::0x2b18::INSTR")
print 'new pm', new_pm.initialized
new_m.close()