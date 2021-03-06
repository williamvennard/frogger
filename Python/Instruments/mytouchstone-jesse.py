"""
This is the "touchstone" module.

The touchstone module supplies one class, Touchstone.  For example,

>>> from touchstone import Touchstone
>>> touch = Touchstone('ERA_1_32mA_Minus45.S2P')
>>> dir(touch)
['FormatError', '__doc__', '__init__', '__module__', 'db_table', 'lines', 'make_json', 'parse']
>>>
"""
import itertools
import json

class Touchstone:
    """Parse Touchstone S2P files

    Returns a class that can parse a touchstone file to json

    >>> from touchstone import Touchstone
    >>> touch = Touchstone('ERA_1_32mA_Minus45.S2P')
    >>> touch.parse()
    >>> touch.options
    ['#', 'MHz', 'S', 'DB', 'R', '50']
    >>> some_json = touch.make_json()
    >>> some_json[-100:]
    '0000", "PHS(S21)": "163.697", "dB(S11)": "-14.706"}}, "options": ["#", "MHz", "S", "DB", "R", "50"]}'
    >>>
    """

    def __init__(self,filename):
        self.filename = filename
        if filename:
            f = open(filename)
            self.lines = f.readlines()
        else:
            self.lines = readlines()

    class FormatError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

    def  parse(self):
        header = []
        option_line = ""
        column_name_line = ""
        column_names = []
        data = {}
        additional_comments = []

        expecting_fields = False
        for line in open(self.filename):
            if line.startswith('!'):
                if expecting_fields:
                    column_names = line.split()[1:]
                    expecting_fields = False
                else:
                    header.append(line)
            elif line.startswith('#'):
                options = line.split()
                if len(options) != 6:
                    raise FormatError("Touchstone file should have 5 options")
                if options[4] != 'R':
                    raise FormatError("Touchstone options missing 'R'")
                self.frequency = options[1]
                self.parameters = options[2]
                self.format = options[3]
                self.ohms = options[5]
                expecting_fields = True
            else:
                if not header:
                    raise FormatError("Touchstone file without column names")
                # OPERATE
                line = line.strip()
                if not line:
                    continue
                values = line.split()
                frequency = values[0]
                if frequency in data:
                    raise FormatError(
                        "Touchstone duplicate frequency: %s" % frequency)
                data[frequency] = dict(zip(column_names,values))  
                self.post(data)
                data = {}
                # POST data
                # data = {}
        self.header = header
        self.options = options
        self.data = data
       
    def post(self, data):
        url = "http://localhost:18080/vnadata/tahoe-vna-2015-06-02-1600"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)

    def make_json(self):
        touchstone_json = json.dumps({'header':self.header,
                                      'options':self.options,
                                      'data':self.data,
                                      'config':'TODO'})
        return touchstone_json

    def db_table(self):
        freqs = self.data.keys()
        freqs.sort(key=float)
        table_spec = """{
            cols: [{id: 'freq', label: 'Frequency', type: 'number'},
                   {id: 'db11', label: 'DB11', type: 'number'},
                   {id: 'db12', label: 'DB12', type: 'number'}],
            rows: ["""
        r = self.data[freqs[0]]
        table_spec += "{c:[{v: '%s'}, {v: '%s'}, {v: '%s'}]}," % (
                      float(freqs[0]),float(r['dB(S11)']),
                      float(r['dB(S12)']))
        rows = []
        for freq in freqs[1:]:
            r = self.data[freq]
            line = "                   "
            line += "{c:[{v: '%s'}, {v: '%s'}, {v: '%s'}]}," % (
                    float(freq),float(r['dB(S11)']),float(r['dB(S12)']))
            rows.append(line)
        table_spec += "\n"
        table_spec += "\n".join(rows)
        table_spec += """
                   ]
        }"""
        return table_spec

def make_db_table():
    """for debugging charts, only"""
    t = Touchstone('ERA_1_32mA_Minus45.S2P')
    t.parse()
    print t.db_table()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
