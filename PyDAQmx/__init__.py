# -*- coding: utf-8 -*-

import DAQmxConfig

from DAQmxTypes import *
from DAQmxConstants import *
from DAQmxFunctions import *
from Task import Task

import DAQmxConstants
import DAQmxFunctions

__all__ = DAQmxConstants.constant_list + DAQmxFunctions.function_dict.keys() + ['Task']

for name in DAQmxConstants.constant_list + DAQmxFunctions.function_dict.keys():
    if name.startswith('DAQmx_'):
        new_name = name[6:]
    elif name.startswith('DAQmx'):
        new_name = name[5:]
    globals()[new_name] = globals()[name]


__version_info__ = (1, 3)
__version__ = '.'.join(str(num) for num in __version_info__)

__author__ =u'Pierre Cladé'
