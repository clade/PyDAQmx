import sys

from ctypes import *
import ctypes
from DAQmxConstants import DAQmx_copyright_year

# New types definitions
# Correspondance between the name used in the NiDAQmx.h file and ctypes
int8 = c_byte
uInt8 = c_ubyte
int16 = c_short
uInt16 = c_ushort 
int32 = c_int 
uInt32 = c_uint 
float32 = c_float 
float64 = c_double 
int64 =c_longlong 
uInt64 = c_ulonglong 
bool32 = uInt32 
if DAQmx_copyright_year<2010:
    TaskHandle = uInt32
else:
    TaskHandle = c_void_p
CalHandle = uInt32

# CFUNCTYPE defined in NIDAQmx.h
DAQmxEveryNSamplesEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
DAQmxDoneEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
DAQmxSignalEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)

class CtypesString(object):
    """ Argtypes to automatically convert str to bytes in Python3 """
    def from_param(self, param):
        if sys.version_info >= (3,):
            if isinstance(param, str):
                param = param.encode('ascii')
        return c_char_p(param)




