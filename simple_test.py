print "Running test without NIDAQmx installed"

import DAQmxConfigTest
from PyDAQmx import *

print DAQmxGetPersistedTaskAttribute(1,2,3,5,4)
