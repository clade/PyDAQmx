import sys
import platform
import os

if sys.platform.startswith('win'):
    # Full path of the NIDAQmx.h file
    # Default location on Windows XP and Windows 7
    dot_h_file = os.environ['PROGRAMFILES']+r'\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h'

    # Name (and eventually path) of the library
    # Default on Windows is nicaiu
    lib_name = "nicaiu"

elif sys.platform.startswith('linux'):
    # On linux you can use the command find_library('nidaqmx')

    # Full path of the NIDAQmx.h file
    dot_h_file = '/usr/local/natinst/nidaqmx/include/NIDAQmx.h'

    # Name (and eventually path) of the library
    lib_name = 'libnidaqmx.so'

else:
    raise NotImplementedError, "Location of niDAQmx library and include file unknown on %s - if you find out, please let the PyDAQmx project know" % (sys.platform)


# If the DAQmxConfigTest has been imported, then uses the value from this file
# This can be used to try different version or compile the module on a plateform where 
# DAQmx is not installed
if "DAQmxConfigTest" in sys.modules.keys():
    from DAQmxConfigTest import *

