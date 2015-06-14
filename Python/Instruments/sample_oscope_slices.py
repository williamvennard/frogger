#
# This sample code will generate names for files, 
# each file spanning 100 milliseconds
# The name of the file is the start of the 100-millisecond interval.
# If a TEK oscope .csv file spans 10 seconds,
# data will be split into 100 files.
# This sample shows how to generate names for data from 7 10-second 
# tek*.csv files. 700 files.
#

import time
from datetime import datetime

def dt2ms(t):
    return int(t.strftime('%s'))*1000 + int(t.microsecond/1000)

t = datetime.strptime("2015-06-12 21:15:10.000", "%Y-%m-%d %H:%M:%S.%f")
print "t.isoformat()=",t.isoformat()
print "t in milliseconds since epoch =",dt2ms(t)
ms = dt2ms(t)

#define range for 7 10-second .csv files in 100-millisecond steps
start = ms
end = start + 7 * 10 * 1000
ms_name_list = [ms for ms in range(start,end,100)]
print "len(ms_name_list) =",len(ms_name_list)
print "ms_name_list[0:10] =",ms_name_list[0:10]
print "ms_name_list[-10:] =",ms_name_list[-10:]

#
# Can also encode in base36 (probably not worth it)
#
def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]

def base36decode(number):
    return int(number,36)

print "base36encode(%d) =" % start, base36encode(start)
encoded_ms = base36encode(start)
print "base36decode(%s) =" % encoded_ms, base36decode(encoded_ms)
base36_name_list = [base36encode(ms) for ms in range(start,end,1000)]
print "base36_name_list[:10] =",base36_name_list[:10]

