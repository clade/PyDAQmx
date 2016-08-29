# -*- coding: utf-8 -*-
import re

from ..config import dot_h_file


class CFunctionPrototype(object):
    __all = []

    def __init__(self, name, arg_string):
        self.name = name
        self.arg_string = arg_string
        self.__all.append(self)

    @classmethod
    def get_all(cls):
        return cls.__all

    def __repr__(self):
        return "{self.name}({self.arg_string})".format(self=self)


def parse_dot_h_file(filename=dot_h_file):
    function_parser = re.compile(r'__CFUNC.* (DAQ\S+)\s*\((.*)\);')
    argsplit = re.compile(', |,')

    with open(dot_h_file, 'r') as include_file:
        for line in include_file:
            fn_match = function_parser.search(line[:-1])
            if fn_match and not line.startswith('//'):
                name = fn_match.group(1)
                arg_string = fn_match.group(2)
                CFunctionPrototype(name, arg_string)


parse_dot_h_file()
