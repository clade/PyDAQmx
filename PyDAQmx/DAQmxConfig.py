import sys
import platform
import os
import ctypes
from ctypes.util import find_library
import platform


dot_h_file = None

NIDAQmxBase = False

if sys.platform.startswith('win') or sys.platform.startswith('cli'):
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
    if 'iron' in platform.python_implementation().lower():
        def get_lib():
            lib_name = "nicaiu"
            DAQlib = ctypes.windll.nicaiu
            DAQlib_variadic = ctypes.cdll.nicaiu
            return DAQlib, DAQlib_variadic
    else:
        def get_lib():
            lib_name = "nicaiu"
            DAQlib = ctypes.windll.LoadLibrary(lib_name)
            DAQlib_variadic = ctypes.cdll.LoadLibrary(lib_name)        
            return DAQlib, DAQlib_variadic


elif sys.platform.startswith('linux'):
    # On linux you can use the command find_library('nidaqmx')

    lib_name = find_library('nidaqmx')
    if lib_name is not None:
        dot_h_file = '/usr/local/natinst/nidaqmx/include/NIDAQmx.h'
        def get_lib():
            lib_name = find_library('nidaqmx')
            DAQlib = ctypes.cdll.LoadLibrary(lib_name)
            DAQlib_variadic = DAQlib
            return DAQlib, DAQlib_variadic



    lib_name = find_library('nidaqmxbase')
    if lib_name is not None:
        dot_h_file = '/usr/local/natinst/nidaqmxbase/include/NIDAQmxBase.h'
        NIDAQmxBase = True
        def get_lib():
            lib_name = find_library('nidaqmxbase')
            ctypes.CDLL('/usr/local/lib/liblvrtdark.so', mode=ctypes.RTLD_GLOBAL)
            DAQlib = ctypes.cdll.LoadLibrary(lib_name)
            DAQlib_variadic = DAQlib
            return DAQlib, DAQlib_variadic

elif sys.platform.startswith('darwin'):
    lib_name = find_library('nidaqmxbase')
    if lib_name is not None:
        dot_h_file = '/Applications/National Instruments/NI-DAQmx Base/includes/NIDAQmxBase.h'
        NIDAQmxBase = True
        def get_lib():
            lib_name = find_library('nidaqmxbase')
            DAQlib = ctypes.cdll.LoadLibrary(lib_name)
            DAQlib_variadic = DAQlib
            return DAQlib, DAQlib_variadic


# If the DAQmxConfigTest has been imported, then uses the value from this file
# This can be used to try different version or compile the module on a plateform where 
# DAQmx is not installed
if "DAQmxConfigTest" in sys.modules.keys():
    from DAQmxConfigTest import *
    if lib_name is None:
        def get_lib():
            class _nothing():
                def __getattr__(self, name):
                    return lambda *args:0
            DAQlib = _nothing()
            DAQlib_variadic = DAQlib
            return DAQlib, DAQlib_variadic

if dot_h_file is None or not os.path.exists(dot_h_file):
    raise NotImplementedError, "Location of niDAQmx library and include file unknown on %s - if you find out, please let the PyDAQmx project know" % (sys.platform)

