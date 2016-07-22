print "Running test without NIDAQmx installed"

import daqmxconfigtest
from pydaqmx import *

print(get_persisted_task_attribute(1,2,3,5,4))

