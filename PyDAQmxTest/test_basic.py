import unittest 
import PyDAQmx


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


