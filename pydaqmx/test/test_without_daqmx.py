""" Test without daqmx

This perform fast test without using daqmx (no functional test are performed)
"""

import unittest
import warnings

from .. import functions
from .. import constants
from .. import errors
from .. import Task, DAQError

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
