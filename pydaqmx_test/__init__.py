import unittest

import pydaqmx
from pydaqmx import *
#from pydaqmx.legacy import *

class TestPyDAQmxBase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(1,1)
    def test_function_list(self):
        self.assertIn("create_task", pydaqmx.functions.__all__)
    def test_constant(self):
        self.assertEqual(pydaqmx.VAL_CFG_DEFAULT,-1) 


suite_base = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxBase)


#class TestError(unittest.TestCase):
#    def test_Device_Invalid(self):
#        t = PyDAQmx.Task()
#        with self.assertRaises(PyDAQmx.DAQError) as cm:
#            t.CreateAIVoltageChan('NonExistingDevice',"", 0,0,0,0,None) 
#        the_exception = cm.exception
#        self.assertEqual(the_exception.error, -200220)

#suite_error = unittest.TestLoader().loadTestsFromTestCase(TestError)

#alltests = unittest.TestSuite([suite_base, suite_error, test_Task.suite, test_variadic.suite])


