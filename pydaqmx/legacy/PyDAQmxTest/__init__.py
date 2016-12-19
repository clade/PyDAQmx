import unittest
import warnings

import PyDAQmx
from . import test_Task
from . import test_variadic
from . import test_misc
from PyDAQmx.example import test as test_examples

class TestPyDAQmxBase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(1,1)
    def test_function_list(self):
        self.assertIn("DAQmxCreateTask", PyDAQmx.function_dict.keys())
    def test_constant(self):
        self.assertEqual(PyDAQmx.DAQmx_Val_Cfg_Default,-1) 
        self.assertEqual(PyDAQmx.Val_Cfg_Default,-1) 
    def test_function_without_prefix(self):
        PyDAQmx.CreateTask



suite_base = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxBase)


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


suite_error = unittest.TestLoader().loadTestsFromTestCase(TestError)

alltests = unittest.TestSuite([suite_base, suite_error, test_Task.suite, test_variadic.suite, test_misc.suite, test_examples.suite])


