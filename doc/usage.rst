.. index:: usage
.. _usage:

==================
How to use PyDAQmx
==================

The PyNIDAQmx module uses ctypes to interface the dll. 

This module uses ctypes to make the interface with DAQmx. We advise to 
user of PyDAQmx to have a look at the documentation of ctypes.

Three modules are defined: 

* :mod:`PyDAQmx.DAQmxTypes`, this module maps the types defined by
  National Instrument to the corresponding ctypes types.
* :mod:`PyDAXmx.DAQmxConstants`, this module imports all the
  predefined constant (like DAQmx_Val_Cfg_Default, DAQmx_Val_Rising,
  etc.) that are defined in the NIDAQmx.h file. 
* :mod:`PyDAQmx.DAQmxFunctions`, this module imports all the funtions
  defined in the NIDAQmx.h file (like DAQmxCreateTask,
  DAQmxCfgSampClkTiming, etc.)

Furthermore, an object oriented interface is introduced in the
:mod:`PyDAQmx.Task` module. See the section :ref:`Task-object`.


Argument types
--------------

All the types used by NI and defined in the NIDAQmx.h file are 
translated to ctypes. You need to import them::

	from PyDAQmx.DAQmxTypes import *

The module convert automatically variable to the right type. You need 
only to declare the type of the variable if it is a pointer.

For example the following C source:: 

	TaskHandle taskHandle=0;
	DAQmxCreateTask("",&taskHandle)

will translate in python as::

	taskHandle = TaskHandle(0)
	DAQmxCreateTask("",byref(taskHandle))

Looking to example provided by NI or the C API help file, there is 
almost a one to one relation between C codes and Python:

	- Constants can be imported from PyDAQmx.DAQmxConstants
	- For variable that are not pointer, use them directly, they will be automatically converted
	- For pointer, declare them first and then use byref
	- NULL in C becomes None in Python

If numpy is installed, PyDAQmx uses numpy arrays for dataArrays instead 
of the ctypes array. This is more efficient.

For example, to read a 1000 long array of float64:

C code::
 
	int32       read;
	float64     data[1000];
	DAQmxReadAnalogF64(taskHandle,1000,10.0,
		DAQmx_Val_GroupByChannel,data,1000,&read,NULL);

PyDAQmx without numpy::

	read =  int32()
	data_type = float64*1000 # define a c_double_Array_1000 type
	data = datatype()
        DAQmxReadAnalogF64(taskHandle,1,10.0,
	    DAQmx_Val_GroupByChannel,data,1,byref(read),None)

PyDAQmx with numpy (recommended way)::

        read = int32()
	data = numpy.zeros((1000,), dtype=numpy.float64)
        DAQmxReadAnalogF64(taskHandle,1,10.0,
	    DAQmx_Val_GroupByChannel,data,1,byref(read),None)


Example
=======

Let us look to a complete example, the Acq-IntClk.c example from AI category (AnalogIn/MeasureVoltage/Acq_IntClk.c)::

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


PyDAQmx automatically deal with error, so a fraction of the C code can 
be removed::

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

The PyDAQmx package indroduce an object oriented interface to the 
DAQmx package. Basically, you replace the taskHandle mecanism with
a Task object. Each function of the NIDAQ that works with a taskHandle
is a method of the Task object. The name is the same without the DAQmx at 
the begining and the taskHandle argument of the function is removed.

The above example now reads:: 

  from PyDAQmx import Task
  from PyDAQmx.DAQmxConstants import *
  from PyDAQmx.DAQmxTypes import *
  import numpy

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


