# -*- coding: utf-8 -*-
from .. import config
from ctypes import create_string_buffer

DAQlib, DAQlib_variadic = config.get_lib()

class DAQError(Exception):
    """Exception raised from the NIDAQ.

    Attributes:
        error -- Error number from NI
        message -- explanation of the error
    """
    def __init__(self, error, mess, fname):
        self.error = error
        self.mess = mess
        self.fname = fname
    def __str__(self):
        return self.mess + '\n in function '+self.fname

def catch_error_default(f):
    def mafunction(*arg):
        error = f(*arg)
        if error<0:
            errBuff = create_string_buffer(2048)
            DAQlib.DAQmxGetExtendedErrorInfo(errBuff,2048)
            raise DAQError(error,errBuff.value.decode("utf-8"), f.__name__)
        elif error>0:
            errBuff = create_string_buffer(2048)
            DAQlib.DAQmxGetErrorString(error, errBuff, 2048);
#            print "WARNING  :",error, "  ", errBuff.value.decode("utf-8")
            raise DAQError(error,errBuff.value.decode("utf-8"), f.__name__)
        return error
    return mafunction

#def catch_error_DAQmxGetSys(f):
#    """ Catch error if the first argument is not None"""
#    default_f = catch_error_default(f)
#    def mafunction(*args):
#        if args[0] is not None:
#            return default_f(*args)
#        return f(*args)
#    return mafunction

def catch_error_buffer(f, data_pos):
    """ Catch error only if the data arg is not None"""
    default_f = catch_error_default(f)
    def mafunction(*args):
        if args[data_pos] is not None:
            return default_f(*args)
        return f(*args)
    return mafunction

def catch_error(f, name, arg_list, arg_name):
#    if name.startswith("DAQmxGetSys"):
#        return catch_error_DAQmxGetSys(f)
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

