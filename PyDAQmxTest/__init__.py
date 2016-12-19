import os
from types import ModuleType
import unittest
import warnings

import PyDAQmx
from . import test_without_daqmx
from . import test_Task
from . import test_variadic
from . import test_misc
from PyDAQmx.example import test as test_examples
from . import test_example

class TestError(unittest.TestCase):
    def test_Device_Invalid(self):
        t = PyDAQmx.Task()
        with self.assertRaises(PyDAQmx.DAQError) as cm:
            t.CreateAIVoltageChan('NonExistingDevice',"", 0,0,0,0,None) 
        the_exception = cm.exception
        self.assertEqual(the_exception.error, -200220)
    def test_Device_Invalid_bis(self):
        t = PyDAQmx.Task()
        with self.assertRaises(PyDAQmx.InvalidDeviceIDError):
            t.CreateAIVoltageChan('NonExistingDevice',"", 0,0,0,0,None) 
    def test_Device_Warning(self):
        t = PyDAQmx.Task()
        t.CreateAOVoltageChan('TestDevice/ao0',"", -5, 5, PyDAQmx.Val_Volts,None)
        t.CfgSampClkTiming("", 2E6, PyDAQmx.Val_Rising, PyDAQmx.Val_ContSamps, 1000)
        with warnings.catch_warnings(record = True) as w:
            t.StartTask()
            self.assertEqual(len(w), 1, 'There should be one warning')  
            self.assertIsInstance(w[-1].message, PyDAQmx.SampClkRateViolatesSettlingTimeForGenWarning)

# This function is called by unittest.main
# Do no delete !!!!
def load_tests(loader, standard_tests, pattern):
    for name, elm in globals().items():
        if name.startswith('test') and isinstance(elm, ModuleType):        
            suite = loader.loadTestsFromModule(elm)
            standard_tests.addTests(suite)
    return standard_tests

