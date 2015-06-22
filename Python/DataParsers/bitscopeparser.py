"""
The bitscopeparser module supplies one class, BitScope.  For example,

>>> from bitscopeparser import BitScope
>>> bits = BitScope('led.bscopedata')
>>> dir(bits)
['__doc__', '__init__', '__module__', 'json', 'lines', 'make_json', 'parse', 'results']
>>> bits.parse()
>>> jdict =  bits.make_json()
>>> jdict[:70]
'{"Capture": "12288 @ 40000000Hz = 0.000307s (LOGIC)\\\\n", "BitScope": "B'
>>>
"""
import json

class FormatError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BitScope:
    """Parse BitScope S2P files

    Returns a class that can parse a bitscope file to json

    >>> from bitscopeparser import BitScope
    >>>
    """

    def __init__(self,filename):
        if filename:
            f = open(filename)
            self.lines = f.readlines()
        else:
            self.lines = readlines()
        self.results = {}
        self.json = ""

    def  parse(self):
        for line in self.lines:
            line = line.lstrip()
            parts = line.split(':')
            if len(parts) < 2:
                raise FormatError(
                   "BitScope line='%s' should have key:value" % line)
            key = parts[0]
            keyparts = key.split('(')
            if keyparts[0] == 'Data':
                key = 'data'
                valparts = keyparts[1].split(')')
                self.results['observations'] = valparts[0]
            value = ":".join(parts[1:])
            value = value.lstrip()
            self.results[key] = value

    def make_json(self):
        self.json = json.dumps(self.results)
        return self.json


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #bscope = BitScope("led.bscopedata")
    #bscope.parse()
    #print bscope.make_json()
    
