# -*- coding: utf-8 -*-
import PyDAQmx as daqmx
from PyDAQmx.DAQmxCallBack import *
import numpy as np
from ctypes import cast

# Sample code to test changing the callback function for a daqmx acquisition
# task. 
#
# Author: Erik Matlin, 9/9/2014
# Modified by Pierre Cladé 23/9/2014

class CallbackWithUnregister(object):
    def __init__(self, device, nSamples=1000):
        self.task = daqmx.Task()
        self.task.EveryNCallback1 = self.EveryNCallback1
        self.task.EveryNCallback2 = self.EveryNCallback2

        self.task.CreateAIVoltageChan("/".join((device,'ai0')), "a", 
            daqmx.DAQmx_Val_Cfg_Default, -10, 10, daqmx.DAQmx_Val_Volts, None)
            

    def start(self, nSamples, callbackname):
        # configure timing
        self.task.CfgSampClkTiming("", 10000, daqmx.DAQmx_Val_Rising, 
            daqmx.DAQmx_Val_ContSamps, nSamples)
        self.nSamples = nSamples
        
        self.task.AutoRegisterEveryNSamplesEvent(daqmx.DAQmx_Val_Acquired_Into_Buffer, nSamples, 0, name=callbackname)                
        self.task.StartTask()
    
    def stop(self):
        self.task.StopTask()
        
    def EveryNCallback1(self):
        read = daqmx.int32(0)
        data = np.zeros(self.nSamples)
        self.task.ReadAnalogF64(self.nSamples, 1.0, 
            daqmx.DAQmx_Val_GroupByScanNumber, data, data.size, 
            daqmx.byref(read), None)
        
    def EveryNCallback2(self):
        read = daqmx.int32(0)
        data = np.zeros(self.nSamples)
        self.task.ReadAnalogF64(self.nSamples, 1.0, 
            daqmx.DAQmx_Val_GroupByScanNumber, data, data.size, 
            daqmx.byref(read), None)


if __name__ == '__main__':
    from time import sleep
    b = CallbackWithUnregister("TestDevice")
    for i,nSamples in enumerate([1000, 2000, 5000]):
        func_name = 'EveryNCallback{0}'.format([1,2][i%2])
        b.start(nSamples, func_name)
        print("started!")
        sleep(.5)
        b.stop()
        print("stop")
