============
Installation
============

First you need to install the NI DAQmx driver provided with your
data-acquisition hardware. Please verify that you have installed together with
the driver the C API (which should be the case by default). Check also that the
C API reference help file is installed.

After installing the driver, you need to find the location of the file
:file:`NIDAQmx.h`. On Windows XP, its location is :file:`C:/Program
Files/National Instruments/NI-DAQ/DAQmx ANSI C/NIDAQmx.h`.  If this not the
case on your system, modify the :file:`DAQmxConfig.py` file in the :file:`PyDAQmx`
module. 

The package also works under linux (but be aware that only a few linux
distributions are supported by National Instruments).

To install PyDAQmx, download the `package`_ and run the command:

.. code-block:: sh

    python setup.py install

You can also directly **move** the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)

It has been reported that the package works on Python 3 using 2to3.  To install
the package with Python 3:

.. code-block:: sh

    2to3 -w setup.py
    python setup.py build
    python setup.py install


.. _package: http://pypi.python.org/pypi/PyDAQmx 
