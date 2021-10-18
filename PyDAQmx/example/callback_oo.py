from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback functions

This example demonstrates how to acquire a continuous amount of 
data using the DAQ device's internal clock. It incrementally store the data 
in a Python list. 

This example is also an example of the object oriented uses of PyDAQmx
"""



# one cannot create a weakref to a list directly
# but the following works well
class MyList(list):
    pass

# list where the data are stored
data = MyList()
id_a = create_callbackdata_id(data)



# Define two Call back functions
def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, callbackData_ptr):
    callbackdata = get_callbackdata_from_id(callbackData_ptr)
    read = int32()
    data = zeros(1000)
    DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByScanNumber,data,1000,byref(read),None)
    callbackdata.extend(data.tolist())
    print("Acquired total %d samples"%len(callbackdata))
    return 0 # The function should return an integer

# Convert the python function to a CFunction      
EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

def DoneCallback_py(taskHandle, status, callbackData):
    print("Status",status.value)
    return 0 # The function should return an integer

# Convert the python function to a CFunction      
DoneCallback = DAQmxDoneEventCallbackPtr(DoneCallback_py)


# Beginning of the script

#DAQmxResetDevice('dev1')

task=Task()
task.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)
task.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)

task.RegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,id_a)
task.RegisterDoneEvent(0,DoneCallback,None)

task.StartTask()

input('Acquiring samples continuously. Press Enter to interrupt\n')

task.StopTask()
task.ClearTask()
