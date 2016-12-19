import unittest
import numpy as np
import ctypes

import pydaqmx
from pydaqmx.test.test_task import _test_for_test_device, test_device_name
from pydaqmx.examples.callback_task_synchronous import CallbackTaskSynchronous


class Test(unittest.TestCase):
    def test(self):
        task=CallbackTaskSynchronous(dev_name=test_device_name)
        task.start_task()

#        print("Acquiring 10 * 1000 samples in continuous mode.")
        for _ in range(10):
            task.get_data(timeout=10.0)
#            print("Acquired %d points" % task.read.value)

        task.stop_task()
        task.clear_task()

