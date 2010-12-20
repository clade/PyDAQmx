===================================
Welcome to PyDAQmx's documentation!
===================================

This package alows users to use data acquisition hardware from `National 
Instrument`_ with Python. It makes an interface between the NIDAQmx driver 
and Python. The package works on Windows and Linux.

The package is not an open source driver for NI acquisition hardware. You first need to install the driver provided by NI.

Compare to similar packages, the PyDAQmx module is a full interface to 
the NIDAQmx ANSI C driver. It imports all the functions from the driver 
and also imports all the predefined constants. This provided an almost 
one to one match between C and Python code.

A more convenient object oriented interface is provided, where the mecanisms 
of taskHandle in C is replace with a :ref:`Task-object`.

The module support callback functions, see :doc:`callback`

Installation
============

You need first to install the NI DAQmx driver which is provided with your 
data-acquisition hardware. Please verify that you have install together with 
the driver the C API (which should be the case by default). 

To install PyDAQmx, download the `package`_ and run the command 

.. code-block:: sh

   python setup.py install

You can also directly **move** the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)

Source code
===========

The `source code <https://github.com/clade/PyDAQmx>`_ is available on GitHub.

Available documentation
=======================

The :doc:`usage` gives you some example on how to use :mod:`PyDAQmx`. 

The part :doc:`installation` describe the installation and configuration of 
:mod:`PyDAQmx`

Contact
=======

Please send bug reports or feedback to `Pierre Cladé`_.



.. toctree::
   :hidden:
   :maxdepth: 1
   
   Overview <self>
   Installation <installation>
   How to use PyDAQmx <usage>
   Example of callback <callback>


.. _National Instrument: http://www.ni.com
.. _Pierre Cladé: mailto:pierre.clade@spectro.jussieu.fr
.. _package: http://pypi.python.org/pypi/PyDAQmx 
