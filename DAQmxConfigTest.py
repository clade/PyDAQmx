import os

# To use non default config parameters or use the PyDAQmx without NIDAQmx isntalled
# Example
# import DAQmxConfigTest
# DAQmxConfigTest.dot_h_file = "..." # optional modification
# import PyDAQmx

lib_name = None

directory = os.path.split(os.path.realpath(__file__))[0]
dot_h_file = os.path.join(directory, "NIDAQmx.h")
