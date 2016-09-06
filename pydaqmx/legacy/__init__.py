# -*- coding: utf-8 -*-

from . import DAQmxConfig

from .DAQmxTypes import *
from .DAQmxConstants import *
from .DAQmxFunctions import *
from .DAQmxErrors import *
from .Task import Task

from . import DAQmxConstants
from . import DAQmxFunctions
from . import DAQmxErrors

all_types = ['int8', 'uInt8', 'int16', 'uInt16', 'int32', 'uInt32', 'float32', 'float64', 'int64', 'uInt64', 'bool32',
        'TaskHandle', 'CalHandle', 'DAQmxEveryNSamplesEventCallbackPtr', 'DAQmxDoneEventCallbackPtr', 'DAQmxSignalEventCallbackPtr', 'CtypesString']


__all__ = DAQmxConstants.constant_list + list(DAQmxFunctions.function_dict.keys()) + ['Task'] + all_types + DAQmxErrors.__all__

for name in DAQmxConstants.constant_list + list(DAQmxFunctions.function_dict.keys()):
    if name.startswith('DAQmx_'):
        new_name = name[6:]
    elif name.startswith('DAQmx'):
        new_name = name[5:]
    globals()[new_name] = globals()[name]


__version_info__ = (1, 3)
__version__ = '.'.join(str(num) for num in __version_info__)

__author__ =u'Pierre Cladé'
