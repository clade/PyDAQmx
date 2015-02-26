# -*- coding: utf-8 -*-
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros
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
        Task.__init__(self)
        if dev_name is None:
            dev_name = "Dev1"
        self._data = zeros(1000)
        self.read = int32()
        self.CreateAIVoltageChan(dev_name+"/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)
        self.CfgSampClkTiming("",100000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
        self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,1000,0)
        self.AutoRegisterDoneEvent(0)
        self._data_lock = threading.Lock()
        self._newdata_event = threading.Event()
    def EveryNCallback(self):
        with self._data_lock:
            self.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByScanNumber,self._data,1000,byref(self.read),None)
            self._newdata_event.set()
        return 0 # The function should return an integer
    def DoneCallback(self, status):
        print "Status",status.value
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
    task.StartTask()

    print "Acquiring 10 * 1000 samples in continuous mode."
    for _ in range(10):
        task.get_data(timeout=10.0)
        print "Acquired %d points" % task.read.value

    task.StopTask()
    task.ClearTask()
