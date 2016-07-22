# -*- coding: utf-8 -*-

from pydaqmx import Task
import pydaqmx
from numpy import zeros
from ctypes import byref
import threading

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example,
illustrating the use of callback functions and the object-oriented Task
interface. It also demonstrates a method of synchronising a main thread with
the asynchronous EveryNCallback.

This example demonstrates how to acquire a continuous amount of data using the
DAQ device's internal clock.
"""

class CallbackTaskSynchronous(Task):
    def __init__(self, dev_name=None, data_len=1000):
        super(CallbackTaskSynchronous, self).__init__()
        if dev_name is None:
            dev_name = "Dev1"
        self._data = zeros(1000)
        self.read = pydaqmx.int32()
        self.create_ai_voltage_chan(dev_name+"/ai0","",pydaqmx.VAL_RSE,-10.0,10.0,pydaqmx.VAL_VOLTS,None)
        self.cfg_samp_clk_timing("",100000.0,pydaqmx.VAL_RISING,pydaqmx.VAL_CONT_SAMPS,1000)
        self.auto_register_every_n_samples_event(pydaqmx.VAL_ACQUIRED_INTO_BUFFER,1000,0)
        self.auto_register_done_event(0)
        self._data_lock = threading.Lock()
        self._newdata_event = threading.Event()
    def every_n_callback(self):
        with self._data_lock:
            self.read_analog_f64(1000,10.0,pydaqmx.VAL_GROUP_BY_SCAN_NUMBER,self._data,1000,byref(self.read),None)
            self._newdata_event.set()
        return 0 # The function should return an integer
    def DoneCallback(self, status):
        print("Status",status.value)
        return 0 # The function should return an integer
    def get_data(self, blocking=True, timeout=None):
        if blocking:
            if not self._newdata_event.wait(timeout):
                raise ValueError("timeout waiting for data from device")
        with self._data_lock:
            self._newdata_event.clear()
            return self._data.copy()


if __name__=="__main__":
    task=CallbackTaskSynchronous()
    task.start_task()

    print("Acquiring 10 * 1000 samples in continuous mode.")
    for _ in range(10):
        task.get_data(timeout=10.0)
        print("Acquired %d points" % task.read.value)

    task.stop_task()
    task.clear_task()
