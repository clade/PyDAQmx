# -*- coding: utf-8 -*-

try:
    from ..native.functions import NativeFunctionMaker
    from ..native.error import DAQError
except ValueError:
    from pydaqmx.native.functions import NativeFunctionMaker
    from pydaqmx.native.error import DAQError

function_dict = {}

for elm in NativeFunctionMaker.get_all():
    globals()[elm.name] = elm.native_function
    function_dict[elm.name] = {'arg_type':elm.arg_ctypes, 'arg_name':elm.arg_names}
    
