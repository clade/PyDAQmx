# -*- coding: utf-8 -*-

try:
    from .native.functions import NativeFunctionMaker
except ImportError:
    from pydaqmx.native.functions import NativeFunctionMaker

__all__ = []

for elm in NativeFunctionMaker.get_all():
    f_name = elm.pep8_name
    globals()[f_name] = elm.pep8_native_function
    __all__.append(f_name)

    
