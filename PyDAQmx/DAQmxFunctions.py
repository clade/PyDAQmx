import re
import sys
from ctypes import *
from DAQmxConfig import dot_h_file, lib_name
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

def catch_error(f):
    def mafunction(*arg):
        error = f(*arg)
        if error<0:
            errBuff = create_string_buffer(2048)
            DAQmxGetExtendedErrorInfo(errBuff,2048)
            raise DAQError(error,errBuff.value.decode("utf-8"), f.__name__)
        elif error>0:
            errBuff = create_string_buffer(2048)
            DAQmxGetErrorString (error, errBuff, 2048);
            print "WARNING  :",error, "  ", errBuff.value.decode("utf-8")
            raise DAQError(error,errBuff.value.decode("utf-8"))

        return error
    return mafunction
if sys.platform.startswith('win'):        
    DAQlib = windll.LoadLibrary(lib_name)
elif sys.platform.startswith('linux'):
    DAQlib = cdll.LoadLibrary(lib_name)
# else other platforms will already have barfed importing DAQmxConfig

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
        return numpy.ctypeslib.ndpointer(dtype = numpy_conversion(string))

################################
#Read the .h file and convert the function for python
################################
include_file = open(dot_h_file,'r') #Open NIDAQmx.h file

################################
# Regular expression to parse the NIDAQmx.h file
# Almost all the function define in NIDAQmx.h file are imported
################################

# Each regular expression is assiciated with a ctypes type and a number giving the 
# group in which the name of the variable is defined


fonction_parser = re.compile(r'.* (DAQ\S+)\s*\((.*)\);')
const_char = re.compile(r'(const char)\s*([^\s]*)\[\]')
string_type = '|'.join(['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64','int64','uInt64','bool32','TaskHandle'])


type_list = ['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64',
    'int64','uInt64','bool32','TaskHandle']
type_list_array = ['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64',
        'int64','uInt64']


# Each regular expression is assAciated with a ctypes type and a number giving the 
# group in which the name of the variable is defined
const_char = [(re.compile(r'(const char)\s*([^\s]*)\[\]'), c_char_p ,2)]
simple_type = [(re.compile('('+_type+')\s*([^\*\[]*)\Z'),eval(_type),2)
     for _type in type_list]
pointer_type = [(re.compile('('+_type+')\s*\*([^\*]*)\Z'),
        eval('POINTER('+_type+')'),2) for _type in type_list]
pointer_type_array = [(re.compile('('+_type+')\s*((?:readArray|writeArray).*)\[\]\Z'),
    array_type(_type),2) for _type in type_list_array]
pointer_type_2 = [(re.compile('('+_type+')\s*([^\s]*)\[\]\Z'),
        eval('POINTER('+_type+')'),2) for _type in type_list]

char_etoile = [(re.compile(r'(char)\s*\*([^\*]*)\Z'), c_char_p, 2)] # match "char * name"
void_etoile = [(re.compile(r'(void)\s*\*([^\*]*)\Z'), c_void_p, 2)] # match "void * name"
char_array = [(re.compile(r'(char)\s*([^\s]*)\[\]'), c_char_p,2)] # match "char name[]"
call_back_A = [(re.compile(r'(DAQmxEveryNSamplesEventCallbackPtr)\s*([^\s]*)'),DAQmxEveryNSamplesEventCallbackPtr ,2)]
call_back_B = [(re.compile(r'(DAQmxDoneEventCallbackPtr)\s*([^\s]*)'),DAQmxDoneEventCallbackPtr,2)]
call_back_C = [(re.compile(r'(DAQmxSignalEventCallbackPtr)\s*([^\s]*)'),DAQmxSignalEventCallbackPtr,2)]


# Create a list with all regular expressions
c_to_ctype_map = []
for l in [const_char, simple_type, pointer_type, pointer_type_array, pointer_type_array,
        pointer_type_2,char_etoile, void_etoile,char_array, 
          call_back_A, call_back_B, call_back_C]:
    c_to_ctype_map.extend(l)



# The list of all function 
# function_dict: the keys are function name, the value is a dictionnary 
# with 'arg_type' and 'arg_name', the type and name of each argument 
function_list = [] 
function_dict = {} 


def _define_function(name, arg_list, arg_name):
    # Record details of function
    function_dict[name] = {'arg_type':arg_list, 'arg_name':arg_name}
    # Fetch C function and apply argument checks
    cfunc = getattr(DAQlib, name)
    setattr(cfunc, 'argtypes', arg_list)
    # Create error-raising wrapper for C function and add to module's dict
    func = catch_error(cfunc)
    func.__name__ = name
    func.__doc__ = '%s(%s) -> error.' % (name, ','.join(arg_name))
    globals()[name] = func



for line in include_file:
    line = line[0:-1]
    if '__CFUNC' in line and fonction_parser.match(line):
        name = fonction_parser.match(line).group(1)
        function_list.append(name)
        arg_string = fonction_parser.match(line).group(2)
        arg_list=[]
        arg_name = []
        for arg in re.split(', ',arg_string):
            for (reg_expr, new_type, groug_nb) in c_to_ctype_map:
                reg_expr_result = reg_expr.search(arg)
                if reg_expr_result is not None:
                    arg_list.append(new_type)
                    arg_name.append(reg_expr_result.group(groug_nb))
                    break # break the for loop
        _define_function(name, arg_list, arg_name)

include_file.close()




# Clean private functions from namespace
del _define_function
