============
Installation
============

You need first to install the NI DAQmx driver which is provided with your 
data-acquisition hardware. Please verify that you have install
the driver the C API (which should be the case by default). Check also that 
the C API reference help file is installed. 

After the installation of the driver, you need to find the location
of the file :file:`NiDAQmx.h`. On Windows XP, it's location is
:file:`C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C\NIDAQmx.h`. 
If this not the case on your system, modify the file :file:`DAQmxConfig.py` in the 
module. 

To install PyDAQmx, download the `package`_ and run the command 

.. code-block:: sh

   python setup.py install

You can also directly **move** the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)


.. _package: http://pypi.python.org/pypi/PyDAQmx 
