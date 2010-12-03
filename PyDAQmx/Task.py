from DAQmxFunctions import *

task_function_list = [name for name in function_dict.keys() if \
                 (function_dict[name]['arg_type'][0] is TaskHandle) and\
                 function_dict[name]['arg_name'][0] =="taskHandle"]

class Task():
    def __init__(self):
        taskHandle = TaskHandle(0)
        DAQmxCreateTask("",byref(taskHandle))
        self.taskHandle = taskHandle


for function_name in task_function_list:
    name = function_name[5:] # remove the DAQmx in front of the name
    exec('Task.%s = lambda self, *args : %s(self.taskHandle,*args)'%(name, function_name))


