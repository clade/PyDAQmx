# -*- coding: utf-8 -*-

try:
    from ..parser import CConstant
except ImportError:
    from pydaqmx.parser import CConstant

constant_list = []

for elm in CConstant.get_all():
    globals()[elm.name] = elm.value
    constant_list.append(elm.name)
