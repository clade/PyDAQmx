""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""

from PyDAQmx import Task
import numpy as np


data = np.array([0,1,1,0,1,0,1,0], dtype=np.uint8)

task = Task()
task.CreateDOChan("/TestDevice/port0/line0:7","",PyDAQmx.DAQmx_Val_ChanForAllLines)
task.StartTask()
task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
task.StopTask()

