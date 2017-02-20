# -*- coding: utf-8 -*-

from .native.types import DAQmxEveryNSamplesEventCallbackPtr, DAQmxDoneEventCallbackPtr, DAQmxSignalEventCallbackPtr, TaskHandle
from ctypes import byref
import ctypes

from . import functions

try :
    from .util.callback_helper import create_callbackdata_id, get_callbackdata_from_id
    _callback = True
except NotImplementedError:
    _callback = False

if _callback:
    class CallbackParent(object):
        _EveryNSamplesEvent_already_register = False
        def auto_register_every_n_samples_event(self, every_n_samples_event_type, n_samples, options, name='every_n_callback'):
#        def AutoRegisterEveryNSamplesEvent(self, everyNsamplesEventType,nSamples,options, name='EveryNCallback'):
            """Register the method named name as the callback function for EveryNSamplesEvent
            
            
            With this method you can register a method of the class Task as a callback function. 
            The parameters every_n_samples_event_type, n_samples and options are the same 
            as the DAQmxRegisterEveryNSamplesEvent parameters
            
            No parameters are passed to the method  

            If an event was already registered, the UnregisterEveryNSamplesEvent is automatically called      
            """
            if self._EveryNSamplesEvent_already_register:
                self.unregister_every_n_samples_event()
            self_id = create_callbackdata_id(self)
            # Define the python function
            def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, self_id):
                self = get_callbackdata_from_id(self_id)
                getattr(self, name)()
                return 0
            # Transform the python function to a CFunction
            self.EveryNCallback_C = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)
            # Register the function
            self.register_every_n_samples_event(every_n_samples_event_type, n_samples, options, self.EveryNCallback_C, self_id)
            self._EveryNSamplesEvent_already_register = True
        def unregister_every_n_samples_event(self):
            self.register_every_n_samples_event(1,0,0,ctypes.cast(None, DAQmxEveryNSamplesEventCallbackPtr),0)
            self._EveryNSamplesEvent_already_register = False

        def auto_register_done_event(self, options, name='done_callback'):
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
            self.register_done_event(options,self.DoneCallback_C,self_id)

        def auto_register_signal_event(self, signal_id, options, name='signal_callback'):
            """Register the method named name as the callback function for RegisterSignalEvent
            
            
            With this method you can register a method of the class Task as a callback function. 
            The parameters signalID, options are the same 
            as the DAQmxRegisterSignalEvent parameters  
            
            No parameter are passed to the method      
            """
            self_id = create_callbackdata_id(self)
            # Define the python function
            def SignalCallback_py(taskHandle, signal_id, self_id):
                self = get_callbackdata_from_id(self_id)
                getattr(self,name)()
                return 0
            # Transform the python function to a CFunction
            self.SignalCallback_C = DAQmxSignalEventCallbackPtr(SignalCallback_py)
            # Register the function
            self.register_signal_event(signalID, options, self.SignalCallback_C, self_id)

else:

    class CallbackParent(object):
        def __getattr__(self, name):
            if name in ['auto_register_every_n_samples_event', 'auto_register_done_event', 'auto_register_signal_event']:
                raise NotImplementedError('Callback methods are not available')
            return super(CallbackParent, self).__getattr__(name)



class Task(CallbackParent):
    def __init__(self, name=""):
        self._task_handle = TaskHandle(0)
        name = name.decode('ASCII')
        functions.create_task(name, byref(self._task_handle))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.clear_task()

    def __del__(self):
        """ Clear automatically the task to be able to reallocate resources """ 
        # Clear the task before deleting the object
        # If the task as already been manually cleared, nothing is done
        # This prevent to clear a task that has a Handle attributed to a new task
        # See this example
        # a = Task(), ..., a.ClearTask(), b = Task(), del(a)
        # b has the same taskHandle as a, and deleting a will clear the task of b   
        try: 
            self.clear_task()
        except DAQError:
            pass
    def clear_task(self):
        if self._task_handle:
            try:
                functions.clear_task(self._task_handle)
            finally:
                self._task_handle.value = 0
    def __repr__(self):
        if self._task_handle:
            return "Task number %d"%self._task_handle.value
        else:
            return "Invalid or cleared Task"
    # Dynamically creates the method
    for name in functions.__all__:
        func = getattr(functions, name)
        maker = func._maker
        if maker.is_task_function:
#            doc = 'Task.{self.pep8_name}(self, {argnames})\n C function is {self.name}'.format(self=maker, argnames=', '.join(maker.pep8_arg_names[1:]))
            arguments = '\n'.join(['    {name}: {typ:s}'.format(name=name, typ=repr(typ)) for name, typ in zip(maker.pep8_arg_names[1:], maker.arg_ctypes[1:])])
            doc = 'C function is {self.name}\n\nArguments:\n{arg}'.format(self=maker, arg=arguments)

            cmd = """def {maker.pep8_name}(self, {args}):
            \"\"\"{doc}\"\"\"
            functions.{maker.pep8_name}(self._task_handle, {args})"""
            exec(cmd.format(maker=maker, doc=doc, args = ', '.join(maker.pep8_arg_names[1:])))    
    del name, func, doc, cmd, maker

