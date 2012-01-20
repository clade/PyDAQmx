from DAQmxTypes import TaskHandle
import DAQmxFunctions
from DAQmxFunctions import *
from DAQmxCallBack import *

# Create a list of the name of the function that uses TastHandle as the firs argument
# All the function of this list will be converted to method of the task object
# The name of the method will be the same name as the name of the DAQmx function without the 
# the DAQmx in front of the name
task_function_list = [name for name in function_dict.keys() if \
                 len(function_dict[name]['arg_type'])>0 and \
                 (function_dict[name]['arg_type'][0] is TaskHandle) and\
                 'task' in function_dict[name]['arg_name'][0]]


class Task():
    def __init__(self):
        taskHandle = TaskHandle(0)
        DAQmxCreateTask(b"",byref(taskHandle))
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
    def AutoRegisterEveryNSamplesEvent(self, everyNsamplesEventType,nSamples,options, name='EveryNCallback'):
        """Register the method named name as the callback function for EveryNSamplesEvent
        
        
        With this method you can register a method of the class Task as a callback function. 
        The parameters everyNsamplesEventType, nSamples and options are the same 
        as the DAQmxRegisterEveryNSamplesEvent parameters
        
        No parameters are passed to the method        
        """
        self_id = create_callbackdata_id(self)
        # Define the python function
        def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, self_id):
            self = get_callbackdata_from_id(self_id)
            getattr(self,name)()
            return 0
        # Transform the python function to a CFunction
        self.EveryNCallback_C = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)
        # Register the function
        self.RegisterEveryNSamplesEvent(everyNsamplesEventType,nSamples,options,self.EveryNCallback_C,self_id)
    def AutoRegisterDoneEvent(self, options, name='DoneCallback'):
        """Register the method named name as the callback function for DoneEvent
        
        With this method you can register a method of the class Task as a callback function. 
        The parameter options is the same as the DAQmxRegisterDoneEvent parameters
        
        The method registered as one parameter, status        
        """
        self_id = create_callbackdata_id(self)
        # Define the python function
        def DoneCallback_py(taskHandle, status, self_id):
            getattr(get_callbackdata_from_id(self_id),name)(status)
            return 0
        # Transform the python function to a CFunction
        self.DoneCallback_C = DAQmxDoneEventCallbackPtr(DoneCallback_py)
        # Register the function
        self.RegisterDoneEvent(options,self.DoneCallback_C,self_id)
    def AutoRegisterSignalEvent(self, signalID, options, name='SignalCallback'):
        """Register the method named name as the callback function for RegisterSignalEvent
        
        
        With this method you can register a method of the class Task as a callback function. 
        The parameters signalID, options are the same 
        as the DAQmxRegisterSignalEvent parameters  
        
        No parameter are passed to the method      
        """
        self_id = create_callbackdata_id(self)
        # Define the python function
        def SignalCallback_py(taskHandle, signalID, self_id):
            self = get_callbackdata_from_id(self_id)
            getattr(self,name)()
            return 0
        # Transform the python function to a CFunction
        self.SignalCallback_C = DAQmxSignalEventCallbackPtr(SignalCallback_py)
        # Register the function
        self.RegisterSignalEvent(signalID, options, self.SignalCallback_C, self_id)


# Remove ClearTask in task_functon_list
task_function_list = [name for name in task_function_list if name not in ['DAQmxClearTask']]

def _create_method(func):
    def _call_method(self,*args):
        return func(self.taskHandle, *args)
    return _call_method


for function_name in task_function_list:
    name = function_name[5:] # remove the DAQmx in front of the name
    func = getattr(DAQmxFunctions, function_name)
    arg_names = function_dict[function_name]['arg_name']
    taskfunc = _create_method(func)
    taskfunc.__name__ = name
    taskfunc.__doc__ = 'T.%s(%s) -> error.' % \
            (name, ', '.join(arg_names[1:]))
    setattr(Task, name, taskfunc)

# Clean private functions from namespace
del _create_method
