from DAQmxTypes import TaskHandle
import DAQmxFunctions
from DAQmxFunctions import *
import ctypes


# Create a list of the name of the function that uses TastHandle as the first argument
# All the function of this list will be converted to method of the task object
# The name of the method will be the same name as the name of the DAQmx function without the 
# the DAQmx in front of the name
task_function_list = [name for name in function_dict.keys() if \
                 len(function_dict[name]['arg_type'])>0 and \
                 (function_dict[name]['arg_type'][0] is TaskHandle) and\
                 'task' in function_dict[name]['arg_name'][0]]

# Remove ClearTask in task_functon_list
task_function_list = [name for name in task_function_list if name not in ['DAQmxClearTask']]

try :
    from DAQmxCallBack import *
    _callback = True
except NotImplementedError:
    _callback = False

if _callback:
    class CallbackParent():
        _EveryNSamplesEvent_already_register = False
        def AutoRegisterEveryNSamplesEvent(self, everyNsamplesEventType,nSamples,options, name='EveryNCallback'):
            """Register the method named name as the callback function for EveryNSamplesEvent
            
            
            With this method you can register a method of the class Task as a callback function. 
            The parameters everyNsamplesEventType, nSamples and options are the same 
            as the DAQmxRegisterEveryNSamplesEvent parameters
            
            No parameters are passed to the method  

            If an event was already registered, the UnregisterEveryNSamplesEvent is automatically called      
            """
            if self._EveryNSamplesEvent_already_register:
                self.UnregisterEveryNSamplesEvent()
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
            self._EveryNSamplesEvent_already_register = True
        def UnregisterEveryNSamplesEvent(self):
            self.RegisterEveryNSamplesEvent(1,0,0,ctypes.cast(None, DAQmxEveryNSamplesEventCallbackPtr),0)
            self._EveryNSamplesEvent_already_register = False

        def AutoRegisterDoneEvent(self, options, name='DoneCallback'):
            """Register the method named name as the callback function for DoneEvent
            
            With this method you can register a method of the class Task as a callback function. 
            The parameter options is the same as the DAQmxRegisterDoneEvent parameters
            
            The method registered has one parameter : status        
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

else:

    class CallbackParent():
        def __getattr__(self, name):
            if name in ['AutoRegisterEveryNSamplesEvent', 'AutoRegisterDoneEvent', 'AutoRegisterSignalEvent']:
                raise NotImplementedError, 'Callback methods are not available'
            return super(CallbackParent, self).__getattr__(name)


class Task(CallbackParent):
    def __init__(self):
        self.taskHandle = TaskHandle(0)
        DAQmxCreateTask(b"",byref(self.taskHandle))
    def __del__(self):
        """ Clear automatically the task to be able to reallocate resources """ 
        # Clear the task before deleting the object
        # If the task as already been manually cleared, nothing is done
        # This prevent to clear a task that has a Handle attributed to a new task
        # See this example
        # a = Task(), ..., a.ClearTask(), b = Task(), del(a)
        # b has the same taskHandle as a, and deleting a will clear the task of b   
        try: 
            self.ClearTask()
        except DAQError:
            pass
    def ClearTask(self):
        if self.taskHandle:
            try:
                DAQmxClearTask(self.taskHandle)
            finally:
                self.taskHandle.value = 0
    def __repr__(self):
        if self.taskHandle:
            return "Task number %d"%self.taskHandle.value
        else:
            return "Invalid or cleared Task"
    # Dynamically creates the method from the task_function_list
    for function_name in task_function_list:
        name = function_name[5:] # remove the DAQmx in front of the name
        func = getattr(DAQmxFunctions, function_name)
        arg_names = function_dict[function_name]['arg_name']
        doc = 'T.%s(%s) -> error.' %(name, ', '.join(arg_names[1:]))
        cmd = """def {0}(self, {1}):
        "{3}"
        {2}(self.taskHandle, {1})"""
        exec(cmd.format(name, ', '.join(arg_names[1:]), function_name, doc))    
    del function_name, name, func, arg_names, doc


del task_function_list
