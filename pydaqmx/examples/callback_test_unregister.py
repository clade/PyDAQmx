# -*- coding: utf-8 -*-

import pydaqmx as daqmx
import numpy as np
import ctypes

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

        self.task.create_ai_voltage_chan("/".join((device,'ai0')), "a", 
            daqmx.VAL_CFG_DEFAULT, -10, 10, daqmx.VAL_VOLTS, None)
            

    def start(self, nSamples, callbackname):
        # configure timing
        self.task.cfg_samp_clk_timing("", 10000, daqmx.VAL_RISING, 
            daqmx.VAL_CONT_SAMPS, nSamples)
        self.nSamples = nSamples
        
        self.task.auto_register_every_n_samples_event(daqmx.VAL_ACQUIRED_INTO_BUFFER, nSamples, 0, name=callbackname)                
        self.task.start_task()
    
    def stop(self):
        self.task.stop_task()
        
    def EveryNCallback1(self):
        read = daqmx.int32(0)
        data = np.zeros(self.nSamples)
        self.task.read_analog_f64(self.nSamples, 1.0, 
            daqmx.VAL_GROUP_BY_SCAN_NUMBER, data, data.size, 
            ctypes.byref(read), None)
        
    def EveryNCallback2(self):
        read = daqmx.int32(0)
        data = np.zeros(self.nSamples)
        self.task.read_analog_f64(self.nSamples, 1.0, 
            daqmx.VAL_GROUPS_BY_SCAN_NUMBER, data, data.size, 
            ctypes.byref(read), None)


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
