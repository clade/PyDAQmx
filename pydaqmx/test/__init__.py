import unittest

from .. import functions
from .. import constants
from .. import Task, DAQError

#from pydaqmx.legacy import *
from . import test_task, test_variadic

class TestPyDAQmxBase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(1,1)
    def test_function_list(self):
        self.assertIn("create_task", functions.__all__)
    def test_constant(self):
        self.assertEqual(constants.VAL_CFG_DEFAULT,-1) 


suite_base = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxBase)


class TestError(unittest.TestCase):
    def test_Device_Invalid(self):
        t = Task()
        with self.assertRaises(DAQError) as cm:
            t.create_ai_voltage_chan('NonExistingDevice',"", 0,0,0,0,None) 
        the_exception = cm.exception
        self.assertEqual(the_exception.error, -200220)

suite_error = unittest.TestLoader().loadTestsFromTestCase(TestError)

alltests = unittest.TestSuite([suite_base, suite_error, test_task.suite, test_variadic.suite])
