import unittest
import PyDAQmx
import ctypes

""" Some functions un PyDAQmx are variadic. PyDAQmx should support them despite 
they have non variadic counterpart (see below). 

"""

class TestVariadic(unittest.TestCase):
    def test_version(self):
        data1 = ctypes.c_uint()
        data2 = ctypes.c_uint()
        PyDAQmx.DAQmxGetSysNIDAQMajorVersion(ctypes.byref(data1))
        PyDAQmx.DAQmxGetSystemInfoAttribute(PyDAQmx.DAQmx_Sys_NIDAQMajorVersion, ctypes.byref(data2))
        self.assertEqual(data1.value, data2.value)
    def test_device_list(self):
        n=1024
        data1 = ctypes.create_string_buffer(n)
        data2 = ctypes.create_string_buffer(n)
        PyDAQmx.DAQmxGetSysDevNames(data1, n)
        PyDAQmx.DAQmxGetSystemInfoAttribute(PyDAQmx.DAQmx_Sys_DevNames, data2, n)
        self.assertEqual(data1.value, data2.value)


suite = unittest.TestLoader().loadTestsFromTestCase(TestVariadic)
