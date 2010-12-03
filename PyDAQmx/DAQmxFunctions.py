import re
from ctypes import *
from DAQmxConfig import dot_h_file
from DAQmxTypes import *

class DAQError(Exception):
    """Exception raised from the NIDAQ.

    Attributes:
        error -- Error number from NI
        message -- explanation of the error
    """
    def __init__(self, error, mess):
        self.error = error
        self.mess = mess
    def __str__(self):
        return self.mess

def catch_error(f):
    def mafunction(*arg):
        error = f(*arg)
        if error<0:
            errBuff = create_string_buffer(2048)
            DAQmxGetExtendedErrorInfo(errBuff,2048)
            raise DAQError(error,errBuff.value)
        elif error>0:
            errBuff = create_string_buffer(2048)
            DAQmxGetErrorString (error, errBuff, 2048);
            print "WARNING  :",error, "  ", errBuff.value
            raise DAQError(error,errBuff.value)

        return error
    return mafunction
        
DAQlib= windll.LoadLibrary("nicaiu.dll")

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
# Exceptions are function containing callbackFunction
################################
fonction_parser = re.compile(r'.* (DAQ\S+)\s*\((.*)\);')
const_char = re.compile(r'(const char)\s*([^\s]*)\[\]')
string_type = '|'.join(['int8','uInt8','int16','uInt16','int32','uInt32','float32','float64','int64','uInt64','bool32','TaskHandle'])

simple_type = re.compile('('+string_type+')\s*([^\*\[]*)\Z')
pointer_type = re.compile('('+string_type+')\s*\*([^\*]*)\Z')
pointer_type2 = re.compile('('+string_type+')\s*([^\s]*)\[\]\Z')
char_etoile = re.compile(r'(char)\s*\*([^\*]*)\Z') # match "char * name"
void_etoile = re.compile(r'(void)\s*\*([^\*]*)\Z') # match "void * name"
char_array = re.compile(r'(char)\s*([^\s]*)\[\]') # match "char name[]"
dots = re.compile('\.\.\.')


function_list = [] # The list of all function 
# function_dict: the keys are function name, the value is a dictionnary 
# with 'arg_type' and 'arg_name', the type and name of each argument 
function_dict = {} 


for line in include_file:
    line = line[0:-1]
    if re.search("int32",line):
        if fonction_parser.match(line):
            name = fonction_parser.match(line).group(1)
            function_list.append(name)
            arg_string = fonction_parser.match(line).group(2)
            if re.search('callbackFunction',arg_string):
                pass # The module do not support callbackFunction
            else:
                arg_list=[]
                arg_name = []
                for arg in re.split(',',arg_string):
                    if const_char.search(arg):
                        arg_list.append(c_char_p)
                        arg_name.append(const_char.search(arg).group(2))
                    elif simple_type.search(arg): 
                        arg_list.append( eval(simple_type.search(arg).group(1)))
                        arg_name.append(simple_type.search(arg).group(2))
                    elif pointer_type.search(arg): 
                        arg_list.append( eval('POINTER('+pointer_type.search(arg).group(1)+')') )
                        arg_name.append(pointer_type.search(arg).group(2))
                    elif pointer_type2.search(arg):
                        if pointer_type2.search(arg).group(2) == 'readArray' or pointer_type2.search(arg).group(2) == 'writeArray':
                            arg_list.append(array_type(pointer_type2.search(arg).group(1)))
                        else:    
                            arg_list.append( eval('POINTER('+pointer_type2.search(arg).group(1)+')') )
                            arg_name.append(pointer_type2.search(arg).group(2))
                    elif char_etoile.search(arg):
                        arg_list.append(c_char_p)
                        arg_name.append(char_etoile.search(arg).group(2))
                    elif void_etoile.search(arg):
                        arg_list.append(c_void_p)
                        arg_name.append(void_etoile.search(arg).group(2))
                    elif char_array.search(arg):
                        arg_list.append(c_char_p)
                        arg_name.append(char_array.search(arg).group(2))
                    elif dots.search(arg):
                        pass
                    else:
                        pass
                function_dict[name] = {'arg_type':arg_list, 'arg_name':arg_name}                
                cmd1 = name+' =  catch_error( DAQlib.'+name+' )'
                cmd2 = 'DAQlib.'+name+'.argtypes = arg_list'
                exec(cmd1)
                exec(cmd2)

include_file.close()

#function_list = function_list[2:]
 




