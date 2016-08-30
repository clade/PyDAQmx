from PyDAQmx.example.AnalogInput_acq_IntClk import *

ai = AIVoltageChan(ai_param=AIParameters(100000, 10000, ['/TestDevice/ai0', '/TestDevice/ai1']), 
                terminalConfig="DAQmx_Val_Diff", 
                trigger=RisingTrigger('/TestDevice/PFI0'))
ai.start()
ai.wait()
ai.read()
ai.stop()
