.. index:: callback
.. _callback:

========================================
How to use callback functions in PyDAQmx
========================================

Callback functions are supported in :mod:`PyDAQmx`. With the function types
defined in :mod:`PyDAQmx.DAQmxTypes`, you can convert a Python function into a
C function pointer or *callback* and pass it to a library function requiring a
callback as an argument, such as :func:`DAQmxRegisterXXXEvent`.

The :mod:`PyDAQmx.DAQmxCallBack` module provides a mechanism for sending data
to a callback function (see the :ref:`second example <send-data-callback>`). If
you want to use a callback, the most effective way is however to use a
:class:`Task` object (see the :ref:`last example <task-object-callback>`).

Examples are available in the GitHub `repository
<https://github.com/clade/PyDAQmx>`_ in the :file:`PyDAQmx/example` directory.

.. note::
    
    Callback are not available with the NIDAQmxBase driver (Linux). You should use the the full NIDAQmx driver.

Simple example
--------------

Using a callback function is a three step problem:

* Define the Python function with the correct arguments
* Create a C function callback for the Python function
* Register the callback within NIDAQmx

This can be performed as follows::

    # Define the python function
    def DoneCallback_py(taskHandle, status, callbackData):
        print "Status",status.value
        return 0 # The function should return an integer

    # Convert the python function to a C function callback
    # The name is defined in DAQmxTypes
    DoneCallback = DAQmxDoneEventCallbackPtr(DoneCallback_py)

    # Register the function
    DAQmxRegisterDoneEvent(taskHandle,0,DoneCallback,None)

.. _send-data-callback:

Send data to a callback function
--------------------------------

NIDAQmx provides a method of passing arbitrary data to a callback function via
the ``callbackData`` argument to the :func:`DAQmxRegisterXXXEvent` functions.

:mod:`PyDAQmx` uses the :mod:`weakref` module to send data to a callback
function. You first need to register your data to get an id that you send to
the callback using the :func:`create_callbackdata_id()` function. You can get
the object back with the :func:`get_callbackdata_from_id()` function.

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

    # Convert the python function to a C function callback
    EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

    DAQmxRegisterEveryNSamplesEvent(taskHandle,DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,id_data)

.. _task-object-callback:

Using a Task object
-------------------

The :mod:`PyDAQmx` module provides an object-oriented interface to the driver
(see the `How to use PyDAQmx <usage>`_ section). With this technique, a
*method* is registered as a callback function. This gives access to all the
attributes of the object inside the callback function.

Here is an example::

    from PyDAQmx import Task
    from numpy import zeros

    """This example is a PyDAQmx version of the ContAcq_IntClk.c example
    It illustrates the use of callback functions

    This example demonstrates how to acquire a continuous amount of
    data using the DAQ device's internal clock. It incrementally stores the data
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
            return 0 # The function should return an integer
        def DoneCallback(self, status):
            print "Status",status.value
            return 0 # The function should return an integer


    task=CallbackTask()
    task.StartTask()

    raw_input('Acquiring samples continuously. Press Enter to interrupt\n')

    task.StopTask()
    task.ClearTask()


