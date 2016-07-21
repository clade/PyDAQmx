# -*- coding: utf-8 -*-
import re
from ctypes import POINTER
from .types import *


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
# Regular expression to parse function prototype
################################

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
c_to_ctypes_map = []
for l in [const_char, simple_type, pointer_type, pointer_type_array, pointer_type_array,
        pointer_type_2, const_char_etoile, char_etoile, void_etoile,char_array,
          call_back_A, call_back_B, call_back_C, variadic]:
    c_to_ctypes_map.extend(l)

##########

