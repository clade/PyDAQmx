# -*- coding: utf-8 -*-
# This file should be compatible with both Python 2 and Python 3
from __future__ import print_function, unicode_literals

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

##### WARNING version string should be modified also in the __init__.py
version = '1.4.6'

import os
directory = os.path.split(os.path.realpath(__file__))[0]
os.chdir(directory)

class Test(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['PyDAQmx']
        self.test_suite = True

    def run_tests(self):
        import unittest

        try:  
            import PyDAQmx
        except NotImplementedError:
            import DAQmxConfigTest

        import PyDAQmx

        print("Functions and constants are imported from : " + PyDAQmx.DAQmxConfig.dot_h_file)

        if PyDAQmx.DAQmxConfig.lib_name is None:
            print('DAQmx is not installed. PyDAQmx is using a dummy library for tests')
            unittest.main('PyDAQmxTest.test_without_daqmx', argv=[unittest.__file__])
        else:
            print("The library is : " + PyDAQmx.DAQmxConfig.lib_name)
            if PyDAQmx.DAQmxConfig.NIDAQmxBase:
                unittest.main('PyDAQmxTest.test_daqmx_base', argv=[unittest.__file__])
            else:
                unittest.main('PyDAQmxTest.test_full', argv=[unittest.__file__])    

class TestExample(TestCommand):
    user_options = [(b'example=', b'm', b"Test example file name")]
    example = 'DEFAULT'
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import unittest

        import PyDAQmx
        import PyDAQmxTest
        execfile(os.path.join(os.path.dirname(PyDAQmxTest.__file__) , self.example))


if sys.version_info >= (3,):
    packages = ["PyDAQmx", 'PyDAQmx.example', 'PyDAQmx.example.test']
else:
    packages = [b"PyDAQmx", b'PyDAQmx.example', b'PyDAQmx.example.test']



long_description = """\
Overview
========

This package allows users to use data acquisition hardware from `National 
Instrument`_ with python. It makes an interface between the NIDAQmx driver 
and python. It currently works only on Windows.

The package is not an open source driver from NI acquisition hardware. You first need to install the driver provided by NI

Compare to similar package, the PyDAQmx module is a full interface to
the NIDAQmx ansi C driver. It imports all the functions from the
driver and also imports all the predefined constants. This provided an
almost one to one match between C and python code. Examples using
callback functions are provided.

A more convenient Object oriented interface is provided, where the mecanism 
of taskHandle in C is replace with a Task object.

**Detailed information** about this package can be found on its `main
website`_.



Installation
============

You need first to install the NI DAQmx driver which is provided with your 
data-acquisition hardware. Please verify that you have install together with 
the driver the C API (which should be the case by default). 

To install PyDAQmx, download the package and run the command:: 

  python setup.py install

You can also directly move the PyDAQmx directory to a location
that Python can import from (directory in which scripts 
using PyDAQmx are run, etc.)
 

Contact
=======

Please send bug reports or feedback to `{auth_name}`_.

Version history
===============
Main changes:

* 1.4.6 Use windows registry to search for files
* 1.4.5 All files compatible with Python 2 and Python 3 (remove 2to3)
* 1.4.4 New location introduced by DAQmx 19
* 1.4.3 Support for Centos 7
* 1.4.2 Proper version string
* 1.4.1 NIDAQmx Base supported on 64bits linux
* 1.4 Many small improvements
* 1.3.2 bug fix
* 1.3.1 With python 3, strings (unicode) can be use as arguments
* 1.3 PyDAQmx supports both the NIDAQmx and NIDAQmxBase drivers
* 1.2.5.2 Bug in version 1.2.5 corrected (Task were not working)
* 1.2.5.1 Add keywords to all the functions (version 1.2.5 is not working with python 3)
* 1.2.4 NIDAQmx functions of the 2011 et 2012 NIDAQmx are imported properly
* 1.2.3 DAQmxAddNetworkDevice is now working
* 1.2.2 The package is working with python 3 using 2to3
* 1.2.1 Add doc string to the DAQmxFunctions
* 1.2 Support of callback function
* 1.1 Add linux support

Version 1.4
===========

Improvements are the following : 

* Each error has a specificc subclass
* Constants can be loaded without the prefix : PyDAQmx.Val_Cfg_Default
* Throw warnings as warnings
* Improve unittest. 

Version 2
=========

A new version of PyDAQmx will is in the dev2 branch on github. PyDAQmx will follow the pep8 naming convention (and will be called pydaqmx). A legacy mode will still be available. 

.. _National Instrument: http://www.ni.com
.. _{auth_name}: mailto:pierre.clade@spectro.jussieu.fr
.. _main website: http://pythonhosted.org/PyDAQmx/
"""

setup_parameters = dict(version=version,
      name = "PyDAQmx",
      author_email="pierre.clade@spectro.jussieu.fr",
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='http://pythonhosted.org/PyDAQmx/',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',
      description='Interface to the National Instruments PyDAQmx driver',
      keywords=['DAQmx', 'National Instrument', 'Data Acquisition','nidaq','nidaqmx'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     packages=packages, 
#     use_2to3=True, 
        cmdclass = {'test': Test, 'test_example':TestExample})

auth_name = "Pierre Cladé"
setup(author=auth_name,
  maintainer=auth_name,
  long_description = long_description.format(auth_name=auth_name), 
  **setup_parameters)

