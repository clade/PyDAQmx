===================================
Welcome to PyDAQmx's documentation!
===================================

This package alows users to use data acquisition hardware from `National 
Instrument`_ with python. It makes an interface between the NIDAQmx driver 
and python. It currently works only with Windows OS.

The package is not an open source driver from NI acquisition hardware. You first need to install the driver provided by NI

Compare to similar package, the PyDAQmx module is a full interface to 
the NIDAQmx ansi C driver. It imports all the functions from the driver 
and also imports all the predefined constants. This provided an almost 
one to one match between C and python code.

A more convenient Object oriented interface is provided, where the mecanism 
of taskHandle in C is replace with a Task object.

Installation
============

You need first to install the NI DAQmx driver which is provided with your 
data-acquisition hardware. Please verify that you have install together with 
the driver the C API (which should be the case by default). 

To install PyDAQmx, download the package and run the command 

.. code-block:: sh

   python setup.py install

You can also directly **move** the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)

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
   Haow to use PyDAQmx <usage>


.. _National Instrument: http://www.ni.com
.. _Pierre Cladé: mailto:pierre.clade@spectro.jussieu.fr

