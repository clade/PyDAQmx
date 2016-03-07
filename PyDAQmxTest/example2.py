""" Simple example of analog output

    This example outputs 'value' on ao0
"""

from PyDAQmx import Task
import numpy as np

value = 1.3

task = Task()
task.CreateAOVoltageChan("/TestDevice/ao0","",-10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
task.StartTask()
task.WriteAnalogScalarF64(1,10.0,value,None)
task.StopTask()

