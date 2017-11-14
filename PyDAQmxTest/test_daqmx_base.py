import unittest
import PyDAQmx
from .test_without_daqmx import TestPyDAQmxBase

class TestPyDAQmxWithoutDAQmx(unittest.TestCase):
    def test_Device_Invalid(self):
        t = PyDAQmx.Task()
        with self.assertRaises(PyDAQmx.DAQError) as cm:
            t.CreateAIVoltageChan('Dev999/ai0',"", 0,0,0,0,None) 
        the_exception = cm.exception
        self.assertEqual(the_exception.error, -200220)
    def test_Device_Invalid_bis(self):
        t = PyDAQmx.Task()
        with self.assertRaises(PyDAQmx.InvalidDeviceIDError):
            t.CreateAIVoltageChan('Dev999/ai0',"", 0,0,0,0,None) 



