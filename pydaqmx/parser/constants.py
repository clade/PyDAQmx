# -*- coding: utf-8 -*-
import re

from ..config import dot_h_file


class CConstant(object):
    __all = []

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.__all.append(self)

    @classmethod
    def get_all(cls):
        return cls.__all

    def __repr__(self):
        return 'CConstant({self.name}, {self.value})'.format(self=self)


def get_copyright_year(filename=dot_h_file):
    # Try get the version of NIDAQmx
    with open(filename, 'r') as include_file:
        preamble = []
        for line in include_file:
            if line.startswith('/*'):
                preamble.append(line)
            else:
                break

    for copyright_line in preamble:
        if "Copyright" in copyright_line:
            DAQmx_copyright_year = max(map(int, re.findall('\d\d\d\d', copyright_line)))
            break
    else:
        DAQmx_copyright_year = 2003
    return DAQmx_copyright_year


def read_constant(filename=dot_h_file):
    define = re.compile(r'\#define\s+(\S+)\s+(".*"|\S+)')
    with open(filename, 'r') as include_file:
        for line in include_file:
            m = define.match(line)
            if m:
                name = m.group(1)
                value = m.group(2)
                try:
                    val = eval(value)
                except NameError:
                    pass
                except SyntaxError:
                    pass
                else:
                    CConstant(name, val)

DAQmx_copyright_year = get_copyright_year()
read_constant()
