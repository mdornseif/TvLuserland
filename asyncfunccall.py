"""Start a funcion in its own thread and get it's returnvalue via an
event."""

__rcsid__ = "$Id: asyncfunccall.py,v 1.3 2002/10/31 22:35:09 drt Exp $"

import sys
import threading
import time
from wxPython.wx import *

myEVT_ASYNCFUNC_DONE = wxNewEventType()

def EVT_ASYNCFUNC_DONE(win, func):
    win.Connect(-1, -1, myEVT_ASYNCFUNC_DONE, func)

class AsyncFuncDoneEvent(wxPyEvent):
    def __init__(self, returnvalue, workerId):
        wxPyEvent.__init__(self)
        self.SetReturnValue(returnvalue)
        self.SetEventType(myEVT_ASYNCFUNC_DONE)
        self.SetWorkerId(workerId)

    #def __del__(self):
    #    print '__del__'
    #    wxPyCommandEvent.__del__(self)

    def SetReturnValue(self, val):
        self.data = val

    def GetReturnValue(self):
        return self.data

    def SetWorkerId(self, val):
        self.workerId = val

    def GetWorkerId(self):
        return self.workerId

class _Worker(threading.Thread):
    def __init__(self, parent, func, *args, **kwargs):
        self.func = func
        self.parent = parent
        self.args = args
        self.kwargs = kwargs
        self.myId = wxNewId()
        threading.Thread.__init__(self)
                    
    def run(self):
        # run the function
        val = apply(self.func, self.args, self.kwargs)
        # raise a event with 'val'
        self.event = AsyncFuncDoneEvent(val, self.myId)
        wxPostEvent(self.parent, self.event)
        # done
    
    def GetId(self):
        return self.myId


def startAsyncFunc(parent, func, *args, **kwargs):
    worker = _Worker(parent, func, *args, **kwargs)
    worker.start()
    return worker.GetId()
    # don'T we have to check if some threads still exist when exiting the programm?
