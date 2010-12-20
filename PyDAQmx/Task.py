from DAQmxFunctions import *

# Create a list of the name of the function that uses TastHandle as the firs argument
# All the function of this list will be converted to method of the task object
# The name of the method will be the same name as the name of the DAQmx function without the 
# the DAQmx in front of the name
task_function_list = [name for name in function_dict.keys() if \
                 (function_dict[name]['arg_type'][0] is TaskHandle) and\
                 'task' in function_dict[name]['arg_name'][0]]


class Task():
    def __init__(self):
        taskHandle = TaskHandle(0)
        DAQmxCreateTask("",byref(taskHandle))
        self.taskHandle = taskHandle
        self.__cleared = False #Flag to clear the task only once
    def __del__(self):
        """ Clear automatically the task to be able to reallocate resources """ 
        # Clear the task before deleting the object
        # If the task as already been manually cleared, nothing is done
        # This prevent to clear a task that has a Handle attributes to a new task
        # See this example
        # a = Task(), ..., a.ClearTask(), b = Task(), del(a)
        # b has the same taskHandle as a, and deleting a will clear the task of b   
        try: 
            if not self.__cleared:
                self.ClearTask()
        except DAQError:
            pass
    def ClearTask(self):
        DAQmxClearTask(self.taskHandle)
        self.__cleared = True
    def __repr__(self):
        return "Task number %d"%self.taskHandle.value

# Remove ClearTask in task_functon_list
task_function_list = [name for name in task_function_list if name not in ['DAQmxClearTask']]

for function_name in task_function_list:
    name = function_name[5:] # remove the DAQmx in front of the name
    exec('Task.%s = lambda self, *args : %s(self.taskHandle,*args)'%(name, function_name))


