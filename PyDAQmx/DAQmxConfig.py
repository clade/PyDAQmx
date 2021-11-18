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
    dot_h_dir_x86, dot_h_dir_x64, dot_h_dir_from_reg = [], [], []
    if 'PROGRAMFILES(X86)' in os.environ:
        dot_h_dir_x86 = [os.path.join(os.environ['PROGRAMFILES(X86)'],
                                      r'National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h'),
                         os.path.join(os.environ['PROGRAMFILES(X86)'],
                                      r'National Instruments\Shared\ExternalCompilerSupport\C\include\NIDAQmx.h')]
    if 'PROGRAMFILES' in os.environ:
        dot_h_dir_x64 = [os.path.join(os.environ['PROGRAMFILES'],
                                      r'National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h'),
                         os.path.join(os.environ['PROGRAMFILES'],
                                      r'National Instruments\Shared\ExternalCompilerSupport\C\include\NIDAQmx.h')]
    try:
        import winreg
    except ImportError:
        winreg = None
    if winreg:
        dirs_from_reg = []
        keys = ((r"SOFTWARE\WOW6432Node\National Instruments\Common\Installer", r"NIDIR"),
                    (r"SOFTWARE\National Instruments\Common\Installer", r"NIDIR64"))
        reg = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        for key in keys:
            try:
                key_open = winreg.OpenKey(reg, key[0])
                var = winreg.QueryValueEx(key_open, key[1])
                dirs_from_reg.append(var[0])
            except FileNotFoundError:
                pass
        for dir in dirs_from_reg:
            dot_h_dir_from_reg.append(os.path.join(dir, r"NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h"))
            dot_h_dir_from_reg.append(os.path.join(dir, r"Shared\ExternalCompilerSupport\C\include\NIDAQmx.h"))

    dot_h_file = None
    for file in dot_h_dir_x64 + dot_h_dir_x86 + dot_h_dir_from_reg:
        if os.path.exists(file): dot_h_file = file

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
        for dot_h_file in ['/usr/include/NIDAQmx.h', 
                           '/usr/local/natinst/nidaqmx/include/NIDAQmx.h']:
            if os.path.exists(dot_h_file):
                break
        else:
            dot_h_file = None
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
            ctypes.CDLL(find_library('lvrtdark'), mode=ctypes.RTLD_GLOBAL)
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
if "DAQmxConfigTest" in list(sys.modules.keys()):
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
    raise NotImplementedError("Location of niDAQmx library and include file unknown on %s - if you find out, please let the PyDAQmx project know" % (sys.platform))

