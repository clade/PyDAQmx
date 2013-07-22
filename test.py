import DAQmxConfigTest
from PyDAQmx import *

task = Task()
task.CreateAIVoltageChan("Dev2/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
