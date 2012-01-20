# -*- coding: utf-8 -*-
import sys

#from distutils.core import setup
from setuptools import setup

version = '1.2.2'

# There is a problem with writing unicode to a file on version of python <2.6
# So I remove the accent of the author name in this case
# TODO: find an automatic way of removing accent if version<2.6
if sys.version_info[:2]>=(2,6): # Unicode accent does not work on earlier version
    setup(name="PyDAQmx", version=version,
      author=u'Pierre Cladé', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer=u'Pierre Cladé',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='http://packages.python.org/PyDAQmx/',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to the National Instrument PyDAQmx driver',

      long_description=u'''\
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

Please send bug reports or feedback to `Pierre Cladé`_.

Version history
===============
Main changes:

* 1.2.2 The package is working with python 3 using 2to3
* 1.2.1 Add doc string to the DAQmxFunctions
* 1.2 Support of callback function
* 1.1 Add linux support


.. _National Instrument: http://www.ni.com
.. _Pierre Cladé: mailto:pierre.clade@spectro.jussieu.fr
.. _main website: http://packages.python.org/PyDAQmx/
''',  
      keywords=['DAQmx', 'National Instrument', 'Data Acquisition','nidaq','nidaqmx'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     packages=["PyDAQmx"]

)
else: # version of python <2.6. Remove the unicode  
      setup(name="PyDAQmx", version=version,
      author='Pierre Clade', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer='Pierre Clade',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='http://packages.python.org/PyDAQmx/',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to the National Instrument PyDAQmx driver',

      long_description='''\
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

Please send bug reports or feedback to `Pierre Clade`_.

Version history
===============
Main changes:

* 1.2.2 The package is working with python 3 using 2to3
* 1.2.1 Add doc string to the DAQmxFunctions
* 1.2 Support of callback function
* 1.1 Add linux support

.. _National Instrument: http://www.ni.com
.. _Pierre Clade: mailto:pierre.clade@spectro.jussieu.fr
.. _main website: http://packages.python.org/PyDAQmx/
''',  
      keywords=['DAQmx', 'National Instrument', 'Data Acquisition','nidaq','nidaqmx'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     packages=["PyDAQmx"]

)
