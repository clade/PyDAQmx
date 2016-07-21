import PyDAQmx
from PyDAQmx import *
import numpy


class AIParameters(object):
    limits = (-10, 10)
    physicalChannel = ["/Dev1/ai0"]

    def __init__(self, sample_rate, sample_number, channels=None, limits=None):
        self.sampleRate = sample_rate
        self.sampleNumber = sample_number
        if limits is None:
            limits = self.limits
        self.limit_inf= limits[0]
        self.limit_sup= limits[1]
        if channels is not None:
            if type(channels) is str:
                physicalChannel = [channels]
            self.physicalChannel = channels

    @property
    def device_name(self):
        device_name = self.physicalChannel[0].split('/')[0]
        if device_name == '' :
            device_name = self.physicalChannel[0].split('/')[1]
        return device_name

class Trigger(object):
    def __init__(self, terminal):
        self.terminal = terminal

class RinsingTrigger(Trigger)
    direction = DAQmx_Val_Rising
         
class FallingTrigger(Trigger)
    direction = DAQmx_Val_Falling


class AIVoltageChan(Task):
    def __init__(self, ai_param, reset=True, terminalConfig=DAQmx_Val_RSE, trigger=None):
        if reset:
            DAQmxResetDevice(ai_param.device_name)
        super(AIVoltageChan, self).__init__(self)
        self.sampleNumber = AIParam.sampleNumber
        self.sampleRate = AIParam.sampleRate
        self.limit_inf = AIParam.limit_inf
        self.limit_sup = AIParam.limit_sup
        self.physicalChannel = AIParam.physicalChannel
        self.numberOfChannel = len(AIParam.physicalChannel)
        if isinstance(terminalConfig, str):
            terminalConfig = getattr(PyDAQmx, terminalConfig)
        self.terminalConfig = terminalConfig
        self.trigger = trigger
        self.configure()
    def configure(self):
        channel_string = ','.join(self.physicalChannel)
        self.CreateAIVoltageChan(channel_string,"",self.terminalConfig,
                                 self.limit_inf,self.limit_sup,
                                 DAQmx_Val_Volts,None)
    def start(self):
        n = self.sampleNumber
        sampleRate = self.sampleRate
        self.CfgSampClkTiming("",sampleRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,n)
        if self.trigger is not None:
            self.CfgDigEdgeRefTrig(self.trigger.terminal,self.trigger.direction,10)
        self.StartTask()
    def read(self):
        n = self.sampleNumber
        data = numpy.zeros((n,self.numberOfChannel), dtype=numpy.float64)
        read = int32()
        self.ReadAnalogF64(n,10.0,DAQmx_Val_GroupByScanNumber,data,n*self.numberOfChannel,byref(read),None)
        return data
    def stop(self):
        self.StopTask()
    def wait(self, timeout=10):
        self.WaitUntilTaskDone(timeout)


if __name__=="__main__":
    ai = AIVoltageChan(param=AiParam(100000, 10000, ['/dev1/ai0', '/dev1/ai1']), 
                    terminalConfig="DAQmx_VAl_PseudoDiff", 
                    trigger=RisingTrigger('/dev1/PFI0'))
    ai.start()
    ai.wait()
    ai.read()
    ai.stop()
