# -*- coding: utf-8 -*-
import re
from ctypes import create_string_buffer

from ..parser import CConstant
from .. import config

DAQlib, DAQlib_variadic = config.get_lib()

class DAQException(Exception):
    """Exception raised from the NIDAQ.

    Attributes:
        error -- Error number from NI
        message -- explanation of the error
    """
    def __init__(self, mess, fname):
        self.mess = mess
        self.fname = fname
    @property
    def error(self):
        """ Returns the error code"""
        # for compatibility with older version
        return self.code
    def __str__(self):
        return self.mess + '\n in function '+self.fname


class DAQError(DAQException):
    pass

error_by_number = {}

class DAQWarning(DAQException, Warning):
    pass

warning_by_number = {}

__all__ = ["DAQError", "DAQWarning", "DAQException"]

for c in CConstant.get_all():
    name = c.name
    if name.startswith('DAQmxError'):
        errname = name[10:]
        error_by_number[c.value] = globals()[errname + 'Error'] = type(errname + 'Error', (DAQError,), dict(code=c.value))
        __all__.append(errname + 'Error')
    elif name.startswith('DAQmxWarning'):
        errname = name[12:]
        warning_by_number[c.value] = globals()[errname + 'Warning'] = type(errname + 'Warning', (DAQWarning,), dict(code=c.value))
        __all__.append(errname + 'Warning')

