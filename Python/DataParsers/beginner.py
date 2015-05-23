### Save for book
# Code below was written by a Python programmer with one month of experience.
# Notes:
# - Variable names not descriptive:
#   - "suff" should be "lines"
#   - "line0" should be "column_names"
#   - "y" should be "fields"
# - The variable "z" is unnecessary.  Should say:
#       values[fields[0]] = dict(zip(column_names, fields))
#   or:
#       frequency = fields[0]
#       values[frequency] = dict(zip(column_names, fields))
# - The "else: return FALSE" is not necessary.  
#   The student put it there because tabs vs. spaces caused indentation errors.
###
import json
filename = 'ERA_1_32mA_Minus45.S2P'
f = open(filename)
stuff = f.readlines()
values = {}
line0 = stuff[8]
for things in stuff[9:]:
    x = things
    y = x.strip().split()
    if y:
        z = dict(zip(line0, y))
        values[y[0]] = z
    else:
        print "FALSE"
jsonvalues = json.dumps(values)
print jsonvalues
