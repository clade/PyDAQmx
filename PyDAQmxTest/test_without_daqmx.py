import DAQmxConfigTest

import unittest
from types import ModuleType

from . import test_basic

def load_tests(loader, standard_tests, pattern):
    for name, elm in globals().items():
        if name.startswith('test') and isinstance(elm, ModuleType):        
            suite = loader.loadTestsFromModule(elm)
            standard_tests.addTests(suite)
    return standard_tests

if __name__=="__main__":
    unittest.main()
