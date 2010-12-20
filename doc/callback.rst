.. index:: callbasjk
.. _callback:

=======================================
How to use callback function in PyDAQmx
=======================================

Callback function are implemented in PyDAQmx. With ctypes, you can
convert a Python function to a CFunction that can be as an argument to
a function loaded with ctypes (The CFunction types are defined in
:mod:`PyDAQmx.DAQmxTypes`).

The :mod:`PyDAQmx.DAQmxCallBack` module provide an mechanism to send
data to the callback function (see the second example)

An complete example is available on the GitHub `repository
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
