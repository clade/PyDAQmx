============
Installation
============

First you need to install the NI DAQmx driver provided with your
data-acquisition hardware. Please verify that you have installed together with
the driver the C API (which should be the case by default). The C API reference
help file is also recommended.

After installing the driver, you need to find the location of the file
:file:`NIDAQmx.h`. On Windows XP its location is
:file:`%ProgramFiles%/National Instruments/NI-DAQ/DAQmx ANSI C/NIDAQmx.h`
(where :envvar:`%ProgramFiles%` is typically :file:`C:/Program Files/`), and on
linux it is assumed to be located at
:file:`/usr/local/natinst/nidaqmx/include/NIDAQmx.h`. If this not the case on
your system, modify the :file:`DAQmxConfig.py` file in the :mod:`PyDAQmx`
module.

The package also works under linux (but be aware that only a few linux
distributions are supported by National Instruments).

To install :mod:`PyDAQmx`, either download the `package`_ manually and run the
command:

.. code-block:: sh

    python setup.py install

or using `pip <http://www.pip-installer.org/>`_:

.. code-block:: sh

    pip install PyDAQmx

You can also directly *move* the :file:`PyDAQmx` directory to a location that
Python can import from (the directory in which scripts using :mod:`PyDAQmx` are
run, :data:`sys.path`, etc.)

It has been reported that the package works on Python 3 using :command:`2to3`.
To install the package with Python 3:

.. code-block:: sh

    python 2to3 -w .
    python setup.py build
    python setup.py install


.. _package: http://pypi.python.org/pypi/PyDAQmx 
