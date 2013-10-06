.. index:: usage
.. _usage:

==================
How to use PyDAQmx
==================

The :mod:`PyDAQmx` module uses :mod:`ctypes` to interface with the NI-DAQmx
dll. We advise users of :mod:`PyDAQmx` to have a look at the documentation of
:mod:`ctypes`.

Three modules are defined: 

* :mod:`PyDAQmx.DAQmxTypes`, this module maps the types defined by National
  Instruments to the corresponding :mod:`ctypes` types.
* :mod:`PyDAXmx.DAQmxConstants`, this module imports all the predefined
  constants (like :data:`DAQmx_Val_Cfg_Default`, :data:`DAQmx_Val_Rising`,
  etc.) that are defined in the :file:`NIDAQmx.h` file.
* :mod:`PyDAQmx.DAQmxFunctions`, this module imports all the functions defined
  in the :file:`NIDAQmx.h` file (like :func:`DAQmxCreateTask()`,
  :func:`DAQmxCfgSampClkTiming()`, etc.)

Furthermore, an object-oriented interface is introduced in the
:mod:`PyDAQmx.Task` module. See the section :ref:`Task-object`.


Argument types
--------------

All the types defined by NI in the :file:`NIDAQmx.h` file are translated to
:mod:`ctypes`. You need to import them::

    from PyDAQmx.DAQmxTypes import *

The module automatically converts variables to the right type. You only need to
declare the type of the variable if it is a pointer.

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
    - For pointers, first declare them and then use :func:`byref()`
    - ``NULL`` in C becomes ``None`` in Python

If :mod:`numpy` is installed, :mod:`PyDAQmx` uses :mod:`numpy` arrays as
``dataArrays`` instead of the :mod:`ctypes` array, as this is more efficient.

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


:mod:`PyDAQmx` automatically handles errors, so some of the C code can be
removed::

    from PyDAQmx import *
    import numpy

    # Declaration of variable passed by reference
    taskHandle = TaskHandle()
    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)

    # DAQmx Configure Code
    DAQmxCreateTask("",byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
    DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

    #DAQmx Start Code
    DAQmxStartTask(taskHandle)

    #DAQmx Read Code
    DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

    print "Acquired %d points\n"%read.value


.. _Task-object:

Task object
===========

The :mod:`PyDAQmx` package introduces an object-oriented interface to the DAQmx
package. Basically, you replace the :data:`taskHandle` mechanism with a
:class:`Task` object. Each function of NIDAQmx that works with a
:data:`taskHandle` is a method of the :class:`Task` object. The method names
are the same as the NIDAQmx function names without the ``DAQmx`` at the
beginning, and the :data:`taskHandle` argument of the function is omitted.

The above example now reads:: 

    from PyDAQmx import Task
    from PyDAQmx.DAQmxConstants import *
    from PyDAQmx.DAQmxTypes import *

    analog_input = Task()
    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)

    #DAQmx Configure Code
    analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
    analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

    #DAQmx Start Code
    analog_input.StartTask()

    #DAQmx Read Code
    analog_input.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

    print "Acquired %d points\n"%read.value


