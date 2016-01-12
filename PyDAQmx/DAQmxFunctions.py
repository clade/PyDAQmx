import re
import sys
from ctypes import *
import warnings

import DAQmxConfig
from DAQmxTypes import *

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
            DAQmxGetExtendedErrorInfo(errBuff,2048)
            raise DAQError(error,errBuff.value.decode("utf-8"), f.__name__)
        elif error>0:
            errBuff = create_string_buffer(2048)
            DAQmxGetErrorString (error, errBuff, 2048);
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


def _add_keywords(arg_name):
    """ This function is used to create a decorator that add arg_name keywords to a function"""
    s = """def add_keywords_decorator(f):
    def function({0}):return f({0})
    return function"""
    exec(s.format(', '.join(arg_name)))
    return locals()['add_keywords_decorator']


#if lib_name is not None:
#    if sys.platform.startswith('win'):        
#        DAQlib = windll.LoadLibrary(lib_name)
#        DAQlib_variadic = cdll.LoadLibrary(lib_name)
#    elif sys.platform.startswith('linux'):
#        DAQlib = cdll.LoadLibrary(lib_name)
#        DAQlib_variadic = DAQlib
#else: # NIDAQmx is not installed on the machine. Use a dummy library
#    class _nothing():
#        def __getattr__(self, name):
#            return lambda *args:0
#    DAQlib = _nothing()
#    DAQlib_variadic = DAQlib
DAQlib, DAQlib_variadic = DAQmxConfig.get_lib()


######################################
# Array
######################################
#Depending whether numpy is install or not, 
#the function array_type is defined to return a numpy array or
#a ctype POINTER
try:
    import numpy
except ImportError:
    def array_type(string):
        return eval('POINTER('+string+')')
else:
    # Type conversion for numpy
    def numpy_conversion(string):
        """ Convert a type given by a string to a numpy type

        """
        #This function uses the fact that the name are the same name, 
        #except that numpy uses lower case
        return eval('numpy.'+string.lower())
    def array_type(string):
        """ Returns the array type required by ctypes when numpy is used """
        return numpy.ctypeslib.ndpointer(dtype = numpy_conversion(string),
                                         flags=('C_CONTIGUOUS','WRITEABLE'))

################################
#Read the .h file and convert the function for python
################################
include_file = open(DAQmxConfig.dot_h_file,'r') #Open NIDAQmx.h file

################################
# Regular expression to parse the NIDAQmx.h file
# Almost all the function define in NIDAQmx.h file are imported
################################

# Each regular expression is assiciated with a ctypes type and a number giving the 
# group in which the name of the variable is defined


function_parser = re.compile(r'__CFUNC.* (DAQ\S+)\s*\((.*)\);')
const_char = re.compile(r'(const char)\s*([^\s]*)\[\]')
string_type = '|'.join(['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64','int64','uInt64','bool32','TaskHandle'])


type_list = ['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64',
    'int64','uInt64','bool32','TaskHandle']
type_list_array = ['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64',
        'int64','uInt64']


# Each regular expression is assAciated with a ctypes type and a number giving the 
# group in which the name of the variable is defined
const_char = [(re.compile(r'(const char)\s*([^\s]*)\[\]'), CtypesString() ,2)]
simple_type = [(re.compile('('+_type+')\s*([^\*\[]*)\Z'),eval(_type),2)
     for _type in type_list]
pointer_type = [(re.compile('('+_type+')\s*\*([^\*]*)\Z'),
        eval('POINTER('+_type+')'),2) for _type in type_list]
pointer_type_array = [(re.compile('('+_type+')\s*((?:readArray|writeArray).*)\[\]\Z'),
    array_type(_type),2) for _type in type_list_array]
pointer_type_2 = [(re.compile('('+_type+')\s*([^\s]*)\[\]\Z'),
        eval('POINTER('+_type+')'),2) for _type in type_list]

const_char_etoile = [(re.compile(r'(const char)\s*\*([^\*]*)\Z'), CtypesString(), 2)] # match "const char * name"
char_etoile = [(re.compile(r'(char)\s*\*([^\*]*)\Z'), c_char_p, 2)] # match "char * name"
void_etoile = [(re.compile(r'(void)\s*\*([^\*]*)\Z'), c_void_p, 2)] # match "void * name"
char_array = [(re.compile(r'(char)\s*([^\s]*)\[\]'), c_char_p,2)] # match "char name[]"
call_back_A = [(re.compile(r'(DAQmxEveryNSamplesEventCallbackPtr)\s*([^\s]*)'),DAQmxEveryNSamplesEventCallbackPtr ,2)]
call_back_B = [(re.compile(r'(DAQmxDoneEventCallbackPtr)\s*([^\s]*)'),DAQmxDoneEventCallbackPtr,2)]
call_back_C = [(re.compile(r'(DAQmxSignalEventCallbackPtr)\s*([^\s]*)'),DAQmxSignalEventCallbackPtr,2)]

variadic = [(re.compile(r'\.\.\.'), "variadic", None)]

# Create a list with all regular expressions
c_to_ctype_map = []
for l in [const_char, simple_type, pointer_type, pointer_type_array, pointer_type_array,
        pointer_type_2, const_char_etoile, char_etoile, void_etoile,char_array,
          call_back_A, call_back_B, call_back_C, variadic]:
    c_to_ctype_map.extend(l)



# The list of all function 
# function_dict: the keys are function name, the value is a dictionnary 
# with 'arg_type' and 'arg_name', the type and name of each argument 
function_list = [] 
function_dict = {} 

def _define_function(name, arg_list, arg_name):
    if "variadic" in arg_list:
        _define_variadic_function(name, arg_list, arg_name)
        return
    # Fetch C function and apply argument checks
    cfunc = getattr(DAQlib, name, None)
    if cfunc is None:
        warnings.warn('Unable to load {0}'.format(name))
        return
    if DAQmxConfig.NIDAQmxBase and 'Base' in name :
        name = name[:5]+name[9:]  
    setattr(cfunc, 'argtypes', arg_list)
    # Create error-raising wrapper for C function and add to module's dict
    func = _add_keywords(arg_name)(catch_error(cfunc, name, arg_list, arg_name))
    func.__name__ = name
    func.__doc__ = '%s(%s) -> error.' % (name, ', '.join(arg_name))
    globals()[name] = func
    # Record details of function
    function_dict[name] = {'arg_type':arg_list, 'arg_name':arg_name}

def _define_variadic_function(name, arg_list, arg_name):
    cfunc = getattr(DAQlib_variadic, name)
    if DAQmxConfig.NIDAQmxBase and 'Base' in name :
        name = name[:5]+name[9:]    
    func = _add_keywords(arg_name)(catch_error(cfunc, name, arg_list, arg_name))
    func.__name__ = name
    func.__doc__ = '%s(%s) -> error.' % (name, ', '.join(arg_name))
    globals()[name] = func
    function_dict[name] = {'arg_type':arg_list, 'arg_name':arg_name}


argsplit = re.compile(', |,')
for line in include_file:
    fn_match = function_parser.search(line[:-1])
    if fn_match and not line.startswith('//'):
        name = fn_match.group(1)
        function_list.append(name)
        arg_string = fn_match.group(2)
        arg_list=[]
        arg_name = []
        for arg in argsplit.split(arg_string): # Almost everywhere there is a space after the comma
            for (reg_expr, new_type, group_nb) in c_to_ctype_map:
                reg_expr_result = reg_expr.search(arg)
                if reg_expr_result is not None:
                    if new_type=="variadic":
                        arg_list.append(new_type)
                        arg_name.append("*args")
                        break
                    arg_list.append(new_type)
                    arg_name.append(reg_expr_result.group(group_nb))
                    break # break the for loop    
        _define_function(name, arg_list, arg_name)

include_file.close()




# Clean private functions from namespace
del _define_function
