===================================
Welcome to PyDAQmx's documentation!
===================================

This package allows users to use data acquisition hardware from `National
Instruments`_ with Python. It provides an interface between the NIDAQmx driver
and Python. The package works on Windows and Linux.

The package is not an open source driver for NI acquisition hardware. You first need to install the driver provided by NI.

Compared to similar packages, the PyDAQmx module is a full interface to the
NIDAQmx ANSI C driver. It imports all the functions from the driver and imports
all the predefined constants. This provides an almost one-to-one match between
C and Python code.

A more convenient object-oriented interface is provided, where the mechanisms
of taskHandle in C is replaced with a :ref:`Task-object`.

The module supports callback functions, see :doc:`callback`

Installation
============

You first need to install the NI DAQmx driver provided with your
data-acquisition hardware. Please verify that you have installed together with
the driver the C API (which should be the case by default).

To install :mod:`PyDAQmx`, download the `package`_ and run the command 

.. code-block:: sh

   python setup.py install

You can also directly *move* the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)

Source code
===========

The `source code <https://github.com/clade/PyDAQmx>`_ is available on GitHub.

Available documentation
=======================

The :doc:`usage` gives you some examples on how to use :mod:`PyDAQmx`.

The part :doc:`installation` describes the installation and configuration of
:mod:`PyDAQmx`.

The part :doc:`callback` gives code examples on how to use callback functions.

Examples are available in the GitHub `repository <https://github.com/clade/PyDAQmx>`_.

Contact
=======

Please send bug reports or feedback to `Pierre Cladé`_.

How to cite this package
========================

If you use this package for a publication (in a journal, on the web, etc.),
please cite it by including as much information as possible from the following:
*PyDAQmx : a Python interface to the National Instruments DAQmx driver*, Pierre
CLADÉ, `http://packages.python.org/PyDAQmx <http://packages.python.org/PyDAQmx>`_.


.. toctree::
   :hidden:
   :maxdepth: 1
   
   Overview <self>
   Installation <installation>
   How to use PyDAQmx <usage>
   Example of callback <callback>


.. _National Instruments: http://www.ni.com
.. _Pierre Cladé: mailto:pierre.clade@spectro.jussieu.fr
.. _package: http://pypi.python.org/pypi/PyDAQmx 
