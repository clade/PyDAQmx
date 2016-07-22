# -*- coding: utf-8 -*-

from .parser import CConstant
from .util import ConstantMaker
from .util import PEP8ConstantName

class PEP8ConstantMaker(ConstantMaker):
    prefix = "DAQmx_"

    @property
    def is_valid(self):
        return self.name.startswith(self.prefix)

    @property
    def pep8_name(self):
        name = self.name_without_prefix
#        if '_' in name[4:]:
#            return name.upper()
        return PEP8ConstantName(name).pep8_name

    @property
    def named_value(self):
        val = self.value
        return globals()['Named'+type(val).__name__.capitalize()](val, self.pep8_name)
            
# Class to record and display the name of the constant
class NamedInt(int):
    def __new__(cls, val, name):
        out = super(NamedInt, cls).__new__(cls, val)
        out.name = name
        return out

    def __repr__(self):
        return self.name

class NamedFloat(float):
    def __new__(cls, val, name):
        out = super(NamedFloat, cls).__new__(cls, val)
        out.name = name
        return out

    def __repr__(self):
        return self.name

class NamedStr(str):
    def __new__(cls, val, name):
        out = super(NamedStr, cls).__new__(cls, val)
        out.name = name
        return out

    def __repr__(self):
        return self.name

       
__all__ = []


for elm in CConstant.get_all():
    cst = PEP8ConstantMaker(elm)
    if cst.is_valid:
        globals()[cst.pep8_name] = cst.named_value
        __all__.append(cst.pep8_name)


