# -*- coding: utf-8 -*-
import warnings

from .. import config
from ctypes import create_string_buffer
from .error import error_by_number, warning_by_number

DAQlib, DAQlib_variadic = config.get_lib()

def catch_error_default(f):
    def mafunction(*arg):
        error = f(*arg)
        if error<0:
            errBuff = create_string_buffer(2048)
            DAQlib.DAQmxGetExtendedErrorInfo(errBuff, 2048)
            raise error_by_number[error](errBuff.value.decode("utf-8"), f.__name__)
        elif error>0:
            errBuff = create_string_buffer(2048)
            DAQlib.DAQmxGetErrorString(error, errBuff, 2048);
#            print "WARNING  :",error, "  ", errBuff.value.decode("utf-8")
            warnings.warn(warning_by_number[error](errBuff.value.decode("utf-8"), f.__name__))
        return error
    return mafunction

def catch_error_buffer(f, data_pos):
    """ Catch error only if the data arg is not None"""
    default_f = catch_error_default(f)
    def mafunction(*args):
        if args[data_pos] is not None:
            return default_f(*args)
        return f(*args)
    return mafunction

def catch_error(f, name, arg_list, arg_name):
    if 'data' in arg_name and 'bufferSize' in arg_name:
        return catch_error_buffer(f, arg_name.index('data'))
    return catch_error_default(f)


def add_keywords(arg_name):
    """ This function is used to create a decorator that add arg_name keywords to a function"""
    s = """def add_keywords_decorator(f):
    def function({0}):return f({0})
    return function"""
    exec(s.format(', '.join(arg_name)))
    return locals()['add_keywords_decorator']

