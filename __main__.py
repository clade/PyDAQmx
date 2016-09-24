import unittest
import argparse

""" Main file use to test the library

For example ::

    python __main__.py 
    python __main__.py legacy

to test the new or legacy version. 

It is also possible to zip the lib obtained with ``python setup.py build``, including this file and run ::

    python lib.zip 

This is usefull to test on a remote system. 

"""

parser = argparse.ArgumentParser(description='Test the PyDAQmx library')

parser.add_argument('version', choices=['pep8', 'legacy'], default='pep8', nargs="?")
parser.add_argument("--shell", help="start an ipython shell",
                    action="store_true")

args = parser.parse_args()

version = args.version
shell = args.shell

if version=='pep8':
    try:  
        import pydaqmx
    except NotImplementedError:
        import daqmxconfigtest

    import pydaqmx
    import pydaqmx.examples
    import pydaqmx.test

    print("Functions and constants are imported from : " + pydaqmx.config.dot_h_file)

    if shell:
        import IPython
        import sys

        IPython.embed()
        sys.exit()

    if pydaqmx.config.lib_name is None:
        print('DAQmx is not installed. pydaqmx is using a dummy library for tests')
    #            unittest.main('PyDAQmxTest', "suite_base", [unittest.__file__])
        unittest.main('pydaqmx.test', "suite_base", [unittest.__file__])
    else:
        print("The library is : " + pydaqmx.config.lib_name)
        unittest.main('pydaqmx.test', "alltests", [unittest.__file__])    
else:
    try:  
        import PyDAQmx
    except NotImplementedError:
        import daqmxconfigtest

    import PyDAQmx

    print("Functions and constants are imported from : " + PyDAQmx.DAQmxConfig.dot_h_file)

    if PyDAQmx.DAQmxConfig.lib_name is None:
        print('DAQmx is not installed. PyDAQmx is using a dummy library for tests')
        unittest.main('PyDAQmx.PyDAQmxTest', "suite_base", [unittest.__file__])
    else:
        print("The library is : " + PyDAQmx.DAQmxConfig.lib_name)
        unittest.main('PyDAQmx.PyDAQmxTest', "alltests", [unittest.__file__])  
