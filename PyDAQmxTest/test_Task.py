import sys
import unittest
import PyDAQmx
import PyDAQmx.example
import ctypes

test_device_name = "TestDevice" # Name of the virtual device use for tests

def _test_for_test_device():
    n = 1024
    buff = ctypes.create_string_buffer(n)
    PyDAQmx.DAQmxGetSysDevNames(buff, n)
    if sys.version_info >= (3,):
        value = buff.value.decode()
    else:
        value = buff.value
    if not test_device_name in map(str.strip, value.split(',')):
        raise Exception('Please install a virtual device called {0} in your system'.format(test_device_name))


class DeviceExists(unittest.TestCase):
    def setUp(self):    
        _test_for_test_device()
    def test_for_test_device(self):
        n = 1024
        buff = ctypes.create_string_buffer(n)
        PyDAQmx.DAQmxGetSysDevNames(buff, n)
        if sys.version_info >= (3,):
            value = buff.value.decode()
        else:
            value = buff.value
        self.assertIn(test_device_name, map(str.strip, value.split(',')))

suiteA = unittest.TestLoader().loadTestsFromTestCase(DeviceExists)

class TestPyDAQmxTask(unittest.TestCase):
    def setUp(self):
        _test_for_test_device()
        self.task = PyDAQmx.Task()
    def tearDown(self):
        self.task.ClearTask()
    def test_CreateAIVoltageChan(self):
        self.task.CreateAIVoltageChan(test_device_name+"/ai0","",PyDAQmx.DAQmx_Val_Cfg_Default,-10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)

suiteB = unittest.TestLoader().loadTestsFromTestCase(TestPyDAQmxTask)

class TestExampleCallbackTaskSynchronous(unittest.TestCase):
    data_len = 1000
    def setUp(self):
        _test_for_test_device()
        self.task = PyDAQmx.example.CallbackTaskSynchronous(dev_name=test_device_name, data_len=self.data_len)
        self.task.StartTask()
    def test_get_data(self):
        reads = []
        n=10
        for _ in range(n):
            self.task.get_data(timeout=10.0)
            reads.append(self.task.read.value)
        self.assertEqual(reads, [self.data_len]*n)
    def tearDown(self):
        self.task.StopTask()
        self.task.ClearTask()

suiteC = unittest.TestLoader().loadTestsFromTestCase(TestExampleCallbackTaskSynchronous)


class TestExampleCallbackWithUnregister(unittest.TestCase):
    def test_truc(self):
        from time import sleep
        b = PyDAQmx.example.CallbackWithUnregister("TestDevice")
        for i,nSamples in enumerate([1000, 2000, 5000]):
            func_name = 'EveryNCallback{0}'.format([1,2][i%2])
            b.start(nSamples, func_name)
#            print "started!"
            sleep(.2)
            b.stop()
#            print "stop"


suiteD = unittest.TestLoader().loadTestsFromTestCase(TestExampleCallbackWithUnregister)

suite = unittest.TestSuite([suiteA, suiteB, suiteC, suiteD])

