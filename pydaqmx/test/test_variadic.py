import unittest
import pydaqmx
import ctypes

""" Some functions un PyDAQmx are variadic. PyDAQmx should support them despite 
they have non variadic counterpart (see below). 

"""

class TestVariadic(unittest.TestCase):
    def test_version(self):
        data1 = ctypes.c_uint()
        data2 = ctypes.c_uint()
        pydaqmx.get_sys_nidaq_major_version(ctypes.byref(data1))
        pydaqmx.get_system_info_attribute(pydaqmx.SYS_NIDAQ_MAJOR_VERSION, ctypes.byref(data2))
        self.assertEqual(data1.value, data2.value)
    def test_device_list(self):
        n=1024
        data1 = ctypes.create_string_buffer(n)
        data2 = ctypes.create_string_buffer(n)
        pydaqmx.get_sys_dev_names(data1, n)
        pydaqmx.get_system_info_attribute(pydaqmx.SYS_DEV_NAMES, data2, n)
        self.assertEqual(data1.value, data2.value)

