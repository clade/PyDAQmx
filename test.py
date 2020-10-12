from __future__ import print_function

try:  
    from PyDAQmx import *
    from PyDAQmx import DAQmxConfig
except NotImplementedError:
    import DAQmxConfigTest
    from PyDAQmx import *
    from PyDAQmx import DAQmxConfig


print("Functions and constants are imported from : ", DAQmxConfig.dot_h_file)

if DAQmxConfig.lib_name is None:
    print('DAQmx is not installed. PyDAQmx is using a dummy library for tests')
else:
    print("The library is : ", DAQmxConfig.lib_name)

task = Task()
task.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)

task.SetTrigAttribute(DAQmx_StartTrig_Retriggerable, True)

#print(help(task.SetTrigAttribute))
print(dir(task))
