import unittest

import PyDAQmx
from . import test_Task
from . import test_variadic

class TestPyDAQmxBase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(1,1)
    def test_function_list(self):
        self.assertIn("DAQmxCreateTask", PyDAQmx.function_dict.keys())
    def test_constant(self):
        self.assertEqual(PyDAQmx.DAQmx_Val_Cfg_Default,-1) 


suite_base = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxBase)


class TestError(unittest.TestCase):
    def test_Device_Invalid(self):
        t = PyDAQmx.Task()
        with self.assertRaises(PyDAQmx.DAQError) as cm:
            t.CreateAIVoltageChan('NonExistingDevice',"", 0,0,0,0,None) 
        the_exception = cm.exception
        self.assertEqual(the_exception.error, -200220)

suite_error = unittest.TestLoader().loadTestsFromTestCase(TestError)

alltests = unittest.TestSuite([suite_base, suite_error, test_Task.suite, test_variadic.suite])


