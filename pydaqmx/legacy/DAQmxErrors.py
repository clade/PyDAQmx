# -*- coding: utf-8 -*-

try:
    from ..native import error
    from ..native.error import *
except ValueError:
    from pydaqmx.native import error
    from pydaqmx.native.error import *

__all__ = error.__all__

