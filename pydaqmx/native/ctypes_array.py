import ctypes
from . import types as my_types

try:
    import numpy
except ImportError:
    numpy = None

if numpy is not None:
    class _cnst_ndptr(numpy.ctypeslib._ndptr):
        """ Used to describe a const array in a C function

        Allow to pass an ndarray, a list or a tuple as function argument
        """
        @classmethod
        def from_param(cls, obj):
            if not isinstance(obj, numpy.ndarray):
                if isinstance(obj, (list, tuple)):
                    obj = numpy.array(obj, dtype=cls._dtype_)
                else:
                    raise TypeError("argument must be an ndarray, a list or a tuple")
            return super(_cnst_ndptr, cls).from_param(obj)

    def ctype_np_array(dtype):
        if isinstance(dtype, str):
            dtype = getattr(numpy, dtype.lower())
        return numpy.ctypeslib.ndpointer(dtype=dtype, flags=('C_CONTIGUOUS','WRITEABLE'))

    def const_ctype_np_array(dtype):
        if isinstance(dtype, str):
            dtype = getattr(numpy, dtype.lower())
        base = numpy.ctypeslib.ndpointer(dtype=dtype, flags=('C_CONTIGUOUS'))
        return type(base.__name__+'_CONSTANT', (_cnst_ndptr, base), {})

def array_pointer(string):
    return eval('POINTER('+string+')')


if numpy is None:
    _const_array_type = array_pointer
    _array_type = array_pointer
else:
    _const_array_type = const_ctype_np_array
    _array_type = ctype_np_array

def const_array_type(str_type):
    if str_type=="void":
        return ctypes.c_void_p
    if str_type=="char":
        return my_types.CtypesString()
    return _const_array_type(str_type)

def array_type(str_type):
    if str_type=="void":
        return ctypes.c_void_p
    if str_type=="char":
        return ctypes.c_char_p
    return _array_type(str_type)

