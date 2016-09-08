# -*- coding: utf-8 -*-
import re
import ctypes

from . import types as my_types
from .ctypes_array import array_type, const_array_type

class Expression(object):
    """ Convert arguments of the C declaration to ctypes"""
    _all = []
    def __init__(self, expr, extract_args):
        self._expr = expr
        self._re = re.compile(expr)
        self._all.append(self)
        self._extract_args = extract_args

    @classmethod
    def get_all(cls):
        return cls._all

    def match(self, s):
        return self._re.match(s)

    def parse(self, s):
        out = self.match(s)
        if out:
            return self._extract_args(out)
        return None



#Expression('const char\s+(?P<var_name>\w+)\s*\[\]$', lambda m:(m.group('var_name'), my_types.CtypesString() )) # const char var[] 
Expression('const char\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), my_types.CtypesString() )) # const char * var
#Expression('char\s+(?P<var_name>\w+)\s*\[\]$', lambda m:(m.group('var_name'), ctypes.c_char_p )) # char var[]
Expression('char\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), ctypes.c_char_p )) # char * var
Expression('void\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), ctypes.c_void_p )) # void * var
Expression('const void\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), ctypes.c_void_p )) # void * var
Expression('(?P<type>\w+)\s+(?P<var_name>\w+)$', lambda m:(m.group('var_name'), getattr(my_types, m.group('type'))))
Expression('(?P<type>\w+)\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), ctypes.POINTER(getattr(my_types, m.group('type')))))
Expression('const\s+(?P<type>\w+)\s*\*\s*(?P<var_name>\w+)$', lambda m:(m.group('var_name'), ctypes.POINTER(getattr(my_types, m.group('type')))))
Expression('(?P<type>\w+)\s+(?P<var_name>\w+)\s*\[\]$', lambda m:(m.group('var_name'), array_type(m.group('type'))))
Expression('const\s+(?P<type>\w+)\s+(?P<var_name>\w+)\s*\[\]$', lambda m:(m.group('var_name'), const_array_type(m.group('type'))))
Expression('\.\.\.$', lambda m:('*args', 'variadic'))

