import sys
import platform
import os


dot_h_file = None

if sys.platform.startswith('win'):
    # Full path of the NIDAQmx.h file
    # Default location on Windows XP and Windows 7
    if os.environ.has_key('PROGRAMFILES(X86)'):
        dot_h_file = os.path.join(os.environ['PROGRAMFILES(X86)'],
                                  r'National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h')
        if not os.path.exists(dot_h_file): dot_h_file = None
    if dot_h_file is None:
        dot_h_file = os.path.join(os.environ['PROGRAMFILES'],
                                  r'National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h')
        if not os.path.exists(dot_h_file): dot_h_file = None

    # Name (and eventually path) of the library
    # Default on Windows is nicaiu
    lib_name = "nicaiu"

    # This is DAQmx based.
    lib_type = 'DAQmx'

    # No extra libs need to be loaded explicitly.
    extra_lib_names = None

elif sys.platform.startswith('linux'):
    # On linux you can use the command find_library('nidaqmx')

    # We could be using either DAQmx or DAQmxBase. Each has a different
    # header and library file. In addition, DAQmxBase requires an extra
    # library to be loaded explicitly first in order to work.

    nidaq_libs = {'DAQmx': {'dot_h_file': '/usr/local/natinst/nidaqmx/include/NIDAQmx.h',
                  'lib_name': '/usr/local/natinst/nidaqmx/lib/libnidaqmx.so',
                  'extra_lib_names': None},
                  'DAQmxBase': {'dot_h_file': '/usr/local/natinst/nidaqmxbase/include/NIDAQmx.h',
                  'lib_name': '/usr/local/natinst/nidaqmxbase/lib/libnidaqmxbase.so',
                  'extra_lib_names': ('/usr/local/lib/liblvrtdark.so',)}}

    if os.path.exists(nidaq_libs['DAQmx']['dot_h_file']):
        lib_type = 'DAQmx'
    elif os.path.exists(nidaq_libs['DAQmxBase']['dot_h_file']):
        lib_type = 'DAQmxBase'
    else:
        raise NotImplementedError, "Location of niDAQmx or niDAQmxBase library and include file unknown on %s - if you find out, please let the PyDAQmx project know" % (sys.platform)

    dot_h_file = nidaq_libs[lib_type]['dot_h_file']
    lib_name = nidaq_libs[lib_type]['lib_name']
    extra_lib_names = nidaq_libs[lib_type]['extra_lib_names']

if dot_h_file is None:
    raise NotImplementedError, "Location of niDAQmx library and include file unknown on %s - if you find out, please let the PyDAQmx project know" % (sys.platform)


# If the DAQmxConfigTest has been imported, then uses the value from this file
# This can be used to try different version or compile the module on a plateform where 
# DAQmx is not installed
if "DAQmxConfigTest" in sys.modules.keys():
    from DAQmxConfigTest import *

