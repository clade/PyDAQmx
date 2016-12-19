import unittest
import numpy as np
import ctypes

import PyDAQmx

from .test_Task import _test_for_test_device, test_device_name

class TestBuffer(unittest.TestCase):
    def test_device_list(self):
        """ Test that one can get the buffer size by sending None as data"""
        n = PyDAQmx.GetSysDevNames(None, 0)
        data = ctypes.create_string_buffer(n)
        PyDAQmx.GetSysDevNames(data, n)

