.. index:: usage
.. _usage:

==================
How to use PyDAQmx
==================

The :mod:`PyDAQmx` module uses :mod:`ctypes` to interface with the NI-DAQmx
dll. We thus advise users of :mod:`PyDAQmx` to read and understand the
documentation of :mod:`ctypes`.

Three core modules are defined, and one higher-level object-oriented module:

* :mod:`PyDAQmx.DAQmxTypes` maps the types defined by National Instruments to
  the corresponding :mod:`ctypes` types (:data:`TaskHandle`,
  :data:`DAQmxEveryNSamplesEventCallbackPtr`, etc.).
* :mod:`PyDAXmx.DAQmxConstants` imports all the constants defined in
  :file:`NIDAQmx.h` (:data:`DAQmx_Val_Cfg_Default`, :data:`DAQmx_Val_Rising`,
  etc.).
* :mod:`PyDAQmx.DAQmxFunctions` imports all the functions defined in
  :file:`NIDAQmx.h` (:func:`DAQmxCreateTask()`,
  :func:`DAQmxCfgSampClkTiming()`, etc.).
* :mod:`PyDAQmx.Task` provides an object-oriented interface to NIDAQmx
  :data:`taskHandle` objects. See the section :ref:`Task-object`.


Argument types
--------------

All the types defined by NI in the :file:`NIDAQmx.h` file are translated to
:mod:`ctypes`, and can be found in the :mod:`PyDAQmx.DAQmxTypes` module::

    from PyDAQmx.DAQmxTypes import *

The module automatically converts variables to the right type. If a library
function requires a pointer, use the :func:`byref()` function to pass
parameters by reference.

For example the following C source:

.. code-block:: c

    TaskHandle taskHandle=0;
    DAQmxCreateTask("",&taskHandle)

will translate into Python as::

    taskHandle = TaskHandle(0)
    DAQmxCreateTask("",byref(taskHandle))

When looking at the C API help file or the examples provided by NI, there is an
almost one-to-one relationship between the C and Python code:

    - Constants can be imported from :mod:`PyDAQmx.DAQmxConstants`
    - Variables that are not pointers can be used directly, as they will be
      automatically converted by :mod:`ctypes`
    - For pointers, first declare them and then use :func:`byref()` to pass by
      reference
    - ``NULL`` in C becomes ``None`` in Python

If :mod:`numpy` is installed, :mod:`PyDAQmx` uses :mod:`numpy` arrays as
``dataArrays`` instead of a :mod:`ctypes` array, as this is more efficient.

For example, to read a 1000 long array of ``float64``:

C code:

.. code-block:: c

    int32       read;
    float64     data[1000];
    DAQmxReadAnalogF64(taskHandle,1000,10.0,
        DAQmx_Val_GroupByChannel,data,1000,&read,NULL);

:mod:`PyDAQmx` without :mod:`numpy`::

    read =  int32()
    data_type = float64*1000 # define a c_double_Array_1000 type
    data = datatype()
    DAQmxReadAnalogF64(taskHandle,1,10.0,
        DAQmx_Val_GroupByChannel,data,1,byref(read),None)

:mod:`PyDAQmx` with :mod:`numpy` (recommended)::

    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)
    DAQmxReadAnalogF64(taskHandle,1,10.0,
        DAQmx_Val_GroupByChannel,data,1,byref(read),None)


Example
=======

To consider a complete example, let's look at the :file:`Acq-IntClk.c` example
from the AI category
(:file:`Analog In/Measure Voltage/Acq-Int Clk/Acq-IntClk.c`):

.. code-block:: c

    #include <stdio.h>
    #include <NIDAQmx.h>

    #define DAQmxErrChk(functionCall) if( DAQmxFailed(error=(functionCall)) ) goto Error; else

    int main(void)
    {
        int32       error=0;
        TaskHandle  taskHandle=0;
        int32       read;
        float64     data[1000];
        char        errBuff[2048]={'\0'};

        /*********************************************/
        // DAQmx Configure Code
        /*********************************************/
        DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
        DAQmxErrChk (DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,NULL));
        DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000));

        /*********************************************/
        // DAQmx Start Code
        /*********************************************/
        DAQmxErrChk (DAQmxStartTask(taskHandle));

        /*********************************************/
        // DAQmx Read Code
        /*********************************************/
        DAQmxErrChk (DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,&read,NULL));

        printf("Acquired %d points\n",read);

    Error:
        if( DAQmxFailed(error) )
            DAQmxGetExtendedErrorInfo(errBuff,2048);
        if( taskHandle!=0 )  {
            /*********************************************/
            // DAQmx Stop Code
            /*********************************************/
            DAQmxStopTask(taskHandle);
            DAQmxClearTask(taskHandle);
        }
        if( DAQmxFailed(error) )
            printf("DAQmx Error: %s\n",errBuff);
        printf("End of program, press Enter key to quit\n");
        getchar();
        return 0;
    }


This translates into Python as::

    from PyDAQmx import *
    import numpy

    # Declaration of variable passed by reference
    taskHandle = TaskHandle()
    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)

    try:
        # DAQmx Configure Code
        DAQmxCreateTask("",byref(taskHandle))
        DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

        # DAQmx Start Code
        DAQmxStartTask(taskHandle)

        # DAQmx Read Code
        DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

        print "Acquired %d points"%read.value
    except DAQError as err:
        print "DAQmx Error: %s"%err
    finally:
        if taskHandle:
            # DAQmx Stop Code
            DAQmxStopTask(taskHandle)
            DAQmxClearTask(taskHandle)

.. note::

   This exemple is for Python 2. In order to use it with Python 3, you should replace strings with binary strings (for example ``b'Dev1/ai0'``)


.. _Task-object:

Task object
===========

The :mod:`PyDAQmx` package introduces an object-oriented interface to the
NIDAQmx package. Basically, you replace the :data:`taskHandle` mechanism with a
:class:`Task` object. Each function of NIDAQmx that works with a
:data:`taskHandle` is a method of the :class:`Task` object. The method names
are the same as the NIDAQmx function names without the ``DAQmx`` at the
beginning, and the :data:`taskHandle` argument of the function is omitted.

The above example now reads::

    from PyDAQmx import *
    import numpy

    analog_input = Task()
    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)

    # DAQmx Configure Code
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

    # DAQmx Start Code
    analog_input.StartTask()

    # DAQmx Read Code
    analog_input.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

    print "Acquired %d points"%read.value

.. note::

    :func:`DAQmxClearTask` is automatically called when a :class:`Task`
    instance is garbage collected, obviating the need to clean up manually.

