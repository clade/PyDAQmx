# -*- coding: utf-8 -*-
from ..parser import CConstant, CFunctionPrototype
from .pep8_conversion import PEP8FunctionName

class Maker(object):
    @property
    def name_without_prefix(self):
        if self.name.startswith(self.prefix):
            return self.name[len(self.prefix):]
        return self.name    

    @classmethod
    def get_all(cls):
        return cls._all


class FunctionMaker(Maker):
#    _all = []
    prefix = 'DAQmx'
    def __init__(self, prototype):
        assert isinstance(prototype,  CFunctionPrototype)
        self._proto = prototype
        self._all.append(self)

    arg_string = property(lambda self:self._proto.arg_string)
    name = property(lambda self:self._proto.name)

    @property
    def pep8_name(self):
        return PEP8FunctionName(self.name_without_prefix).pep8_name




class ConstantMaker(Maker):
    _all = []
    def __init__(self, c_cst):
        assert isinstance(c_cst,  CConstant)
        self._c_cst = c_cst
        self._all.append(self)

    name = property(lambda self:self._c_cst.name)
    value = property(lambda self:self._c_cst.value)

    @property
    def type_(self):
        return type(self.value)


