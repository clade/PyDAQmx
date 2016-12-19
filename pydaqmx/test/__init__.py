import os
from types import ModuleType

import unittest
import warnings

from .. import functions
from .. import constants
from .. import errors
from .. import Task, DAQError

# You should explicitely import all modules containing tests
from . import test_task, test_variadic, test_misc, test_without_daqmx
from ..examples import test_callback_task_synchronous


class TestError(unittest.TestCase):
    def test_Device_Invalid(self):
        t = Task()
        with self.assertRaises(DAQError) as cm:
            t.create_ai_voltage_chan('NonExistingDevice',"", 0,0,0,0,None) 
        the_exception = cm.exception
        self.assertEqual(the_exception.code, -200220)
    def test_Device_Invalid_bis(self):
        t = Task()
        with self.assertRaises(errors.InvalidDeviceIDError):
            t.create_ai_voltage_chan('NonExistingDevice',"", 0,0,0,0,None) 
    def test_Device_Warning(self):
        t = Task()
        t.create_ao_voltage_chan('TestDevice/ao0',"", -5,5,constants.VAL_VOLTS,None)
        t.cfg_samp_clk_timing("", 2E6, constants.VAL_RISING, constants.VAL_CONT_SAMPS, 1000)
        with warnings.catch_warnings(record = True) as w:
            t.start_task()
            self.assertEqual(len(w), 1, 'There should be one warning')  
            self.assertIsInstance(w[-1].message, errors.SampClkRateViolatesSettlingTimeForGenWarning)

# This function is called by unittest.main
# Do no delete !!!!
def load_tests(loader, standard_tests, pattern):
    for name, elm in globals().items():
        if name.startswith('test') and isinstance(elm, ModuleType):        
            suite = loader.loadTestsFromModule(elm)
            standard_tests.addTests(suite)
    return standard_tests
