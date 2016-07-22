# -*- coding: utf-8 -*-

def split_name(full_name):
        out_f = []
        for name in magic_split(full_name):
            out = []
            tmp = ""
            for ch in reversed(name):
    #            print self.name, ch, tmp
                if ch.islower() and tmp.isupper():
                    out.insert(0, tmp)
                    tmp = ""
                tmp = ch + tmp
                if ch.isupper() and not tmp.isupper():
                    out.insert(0, tmp)
                    tmp = ""
            if tmp:
                out.insert(0, tmp)
            out_f.extend(out)
        return out_f  


magic = ['dB', 'IDs', 'GPS', 'AI', 'CI', 'DAQmx']

def magic_split(name_ini):
    for name in name_ini.split('_'):
        for elm in magic:
            if elm in name:
                deb, fin = name.split(elm, 1)
                yield deb
                yield elm.lower()
                for e in magic_split(fin):
                    yield e
                return
        else:
            yield name


class PEP8FunctionName(object):
    def __init__(self, name):
        self.name = name

    @property
    def pep8_name(self):
        return '_'.join([elm.lower() for elm in split_name(self.name)])

class PEP8ConstantName(object):
    def __init__(self, name):
        self.name = name

    @property
    def pep8_name(self):
        return '_'.join([elm.upper() for elm in split_name(self.name)])

class PEP8ArgName(object):
    def __init__(self, name):
        self.name = name

    @property
    def pep8_name(self):
        return '_'.join([elm.lower() for elm in split_name(self.name)])


