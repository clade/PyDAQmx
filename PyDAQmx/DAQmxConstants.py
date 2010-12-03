""" Initialize the constants from the NIDAQmx.h file

Read the NIDAQmx.h file and "execute" the #define command
"""

import re
from DAQmxConfig import dot_h_file

include_file = open(dot_h_file,'r') #Open NIDAQmx.h file

# Regular expression to parse the #define line
# Parse line like : #define PI 3.141592
# The first group is the name of the constant
# The second group the value
define = re.compile(r'\#define (\S+)\s*(".*"|\S*)')
notempty = re.compile(r'\S')

# List containing all the name of the constant
constant_list = []

for line in include_file:
    if re.match('\#define',line):
        a = define.match(line)
        if a:
           name = define.match(line).group(1)
           value = define.match(line).group(2)
           if notempty.match(value):
               try:
                   exec(name +'='+value)
               except NameError:
                   pass
               except SyntaxError:
                   pass
               else:
                   constant_list.append(name)
    
include_file.close()
