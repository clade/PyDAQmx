import unittest
import warnings

from .. import functions
from .. import constants
from .. import errors
from .. import Task, DAQError

#from pydaqmx.legacy import *
from . import test_task, test_variadic, test_misc

class TestPyDAQmxBase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(1,1)
    def test_function_list(self):
        self.assertIn("create_task", functions.__all__)
    def test_constant(self):
        self.assertEqual(constants.VAL_CFG_DEFAULT,-1) 
    def test_error_list(self):
        self.assertIn("ReadNotCompleteBeforeSampClkError", errors.__all__)
    def test_warning_list(self):
        self.assertIn("AISampRateTooLowWarning", errors.__all__)

suite_base = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxBase)


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

suite_error = unittest.TestLoader().loadTestsFromTestCase(TestError)

alltests = unittest.TestSuite([suite_base, suite_error, test_task.suite, test_variadic.suite, test_misc.suite])
