.. index:: callback
.. _callback:

=======================================
How to use callback function in PyDAQmx
=======================================

Callback function are implemented in PyDAQmx. With ctypes, you can
convert a Python function to a CFunction that can be as an argument to
a function loaded with ctypes (The CFunction types are defined in
:mod:`PyDAQmx.DAQmxTypes`).

The :mod:`PyDAQmx.DAQmxCallBack` module provide an mechanism to send
data to the callback function (see the second example). If you want to use
callback, the most effective way is to use a Task object (see the last example). 

Examples are available on the GitHub `repository
<https://github.com/clade/PyDAQmx>`_, in the :file:`PyDAQmx\example`
directory.

Simple example
--------------

Using a callback function is a three steps problem:

* Define the Python function, with the correct arguments
* Transform the function to a CFunction
* Regiter the call back within NIDAQmx

Here is the code::
     
    # Define the python function
    def DoneCallback_py(taskHandle, status, callbackData):
        print "Status",status.value
	return 0 # The function should return an integer
	 
    # Convert the python function to a CFunction
    # The name is defined in DAQmxTypes
    DoneCallback = DAQmxDoneEventCallbackPtr(DoneCallback_py)

    # Register the function
    DAQmxRegisterDoneEvent(taskHandle,0,DoneCallback,None)

Send data to a callback function
--------------------------------

:mod:`PyDAQmx` uses the :mod:`weakref` module to send data to a
callback function. You need to first register your data to get an id
that you send to the function (function
:mod:`create_callbackdata_id`). Then you can get the object back with
the function :mod:`get_callbackdata_from_id`.

Here is an example::

     from PyDAQmx.DAQmxCallBack import *
     from numpy import zeros

     # Class of the data object
     # one cannot create a weakref to a list directly
     # but the following works well
     class MyList(list):
         pass

     # list where the data are stored
     data = MyList()
     id_data = create_callbackdata_id(data)

     def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, callbackData_ptr):
     	 callbackdata = get_callbackdata_from_id(callbackData_ptr)
	 read = int32()
	 data = zeros(1000)
	 DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByScanNumber,data,1000,byref(read),None)
	 callbackdata.extend(data.tolist())
	 print "Acquired total %d samples"%len(data)
	 return 0 # The function should return an integer

     # Convert the python function to a CFunction      
     EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

     DAQmxRegisterEveryNSamplesEvent(taskHandle,DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,id_data)

Using a Task object
-------------------

The :mod:`PyDAQmx` module provides an object oriented interface the the driver (see the `How to use PyDAQmx <usage>`_ section). With this technique, a method is registered as a call back function. This give acces to all the attibutes of the object inside the callback function. 

Here is an example::

    from PyDAQmx import Task
    from numpy import zeros

    """This example is a PyDAQmx version of the ContAcq_IntClk.c example
    It illustrates the use of callback function

    This example demonstrates how to acquire a continuous amount of
    data using the DAQ device's internal clock. It incrementally store the data
    in a Python list.
    """

    class CallbackTask(Task):
        def __init__(self):
            Task.__init__(self)
            self.data = zeros(1000)
            self.a = []
            self.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)
            self.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
            self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,1000,0)
            self.AutoRegisterDoneEvent(0)
        def EveryNCallback(self):
            read = int32()
            self.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByScanNumber,self.data,1000,byref(read),None)
            self.a.extend(self.data.tolist())
            print self.data[0]
        def DoneCallback(self, status):
            print "Status",status.value
            return 0 # The function should return an integer


    task=CallbackTask()
    task.StartTask()

    raw_input('Acquiring samples continuously. Press Enter to interrupt\n')

    task.StopTask()
    task.ClearTask()


