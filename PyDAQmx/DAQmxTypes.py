from ctypes import *

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
TaskHandle = uInt32

# CFUNCTYPE defined in NIDAQmx.h
DAQmxEveryNSamplesEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
DAQmxDoneEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
DAQmxSignalEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)