"""Start a funcion in its own thread and get it's returnvalue via an
event."""

import sys
import threading
import time
from wxPython.wx import *

myEVT_ASYNCFUNC_DONE = wxNewEventType()

def EVT_ASYNCFUNC_DONE(win, parent, func):
    win.Connect(parent, -1, myEVT_ASYNCFUNC_DONE, func)

class AsyncFuncDoneEvent(wxPyEvent):
    def __init__(self):
        wxPyEvent.__init__(self)
        self.myVal = None

    #def __del__(self):
    #    print '__del__'
    #    wxPyCommandEvent.__del__(self)

    def SetReturnValue(self, val):
        self.data = val

    def GetReturnValue(self):
        return self.data

class Worker(threading.Thread):
    def __init__(self, parent, func, *args, **kwargs):
        self.func = func
        self.parent = parent
        self.args = args
        self.kwargs = kwargs
        self.myId = wxNewId()
        self.event = AsyncFuncDoneEvent()
        threading.Thread.__init__(self)
                    
    def run(self):
        sleep(10)
        # run the function
        val = apply(self.func, self.args, self.kwargs)
        # raise a event with 'val'
        self.event.SetReturnValue(val)
        wxPostEvent(self,parent, self.event)
        # done
    
    def GetId(self):
        return self.myId


def startAsyncFunc(parent, func, *args, **kwargs):
    worker = Worker(parent, func, *args, **kwargs)
    return worker.GetId()
