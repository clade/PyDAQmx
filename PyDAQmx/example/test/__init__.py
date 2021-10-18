import os
from types import ModuleType
import unittest


from . import test_MultiChannelAnalogInput

#suite = unittest.TestSuite([test_MultiChannelAnalogInput.suite])


# This function is called by unittest.main
# Do no delete !!!!
def load_tests(loader, standard_tests, pattern):
    for name, elm in list(globals().items()):
        if name.startswith('test') and isinstance(elm, ModuleType):        
            suite = loader.loadTestsFromModule(elm)
            standard_tests.addTests(suite)
    return standard_tests

