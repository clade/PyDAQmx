============
Installation
============

First you need to install the NI DAQmx driver provided with your
data-acquisition hardware. Please verify that you have installed together with
the driver the C API (which should be the case by default). The C API reference
help file is also recommended.

After installing the driver, you need to find the location of the file
:file:`NIDAQmx.h`. Default locations are available for Windows and Linux. 
If the default location doesn't work for your system, modify the :file:`DAQmxConfig.py` file in the :mod:`PyDAQmx`
module.

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

Python 3
--------

The package works on Python 3 using :command:`2to3`.
To install the package with Python 3:

.. code-block:: sh

    python setup.py build
    python setup.py install


Linux
-----

The package also works under linux. Only a few linux
distributions are supported by National Instruments. Furthermore, the full NIDAQmx driver is no longer available. Only the restricted NIDAQmxBase is available. 

The PyDAQmx package is compatible with both driver. If the NIDAQmxBase is used, then the name of the function are modified so that it is compatible with the NIDAQmx driver. 

The package is tested against NIDAQmxBase installed on `Scientific Linux 6 <https://www.scientificlinux.org/>`_.



.. _package: http://pypi.python.org/pypi/PyDAQmx 
