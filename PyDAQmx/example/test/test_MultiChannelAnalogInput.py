import unittest

from ..MultiChannelAnalogInput import MultiChannelAnalogInput

class Test(unittest.TestCase):
    def test(self):
        multipleAI = MultiChannelAnalogInput(["TestDevice/ai2","TestDevice/ai1"],  reset=True)
        multipleAI.configure()
        multipleAI.read("TestDevice/ai2")


suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(Test)])

