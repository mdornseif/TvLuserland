__rcsid__ = "$Id: TvDebug.py,v 1.1 2002/11/09 08:34:26 drt Exp $"

import tv

from wxPython.wx import *
from wxPython.lib.PyCrust.shell import Shell
from wxPython.lib.PyCrust.filling import Filling

class ShellFrame(wxFrame):  
    def __init__(self, parent, parentApp):  
        wxFrame.__init__(self, parent, -1, "Tv Shell",
                             pos=wxDefaultPosition, 
                             size=wxDLG_SZE(parent, 300, 200))  
          
        parentApp.shell = Shell(self, -1)  
        parentApp.shell.interp.locals['app'] = parentApp  
        parentApp.shell.interp.locals['tv'] = tv  
        self.parentApp = parentApp  
  
        wx.EVT_CLOSE(self, self.onCloseMe)  
  
    def onCloseMe(self, evt):  
        self.Show(0)  


class InspectorFrame(wxFrame):  
    def __init__(self, parent, parentApp):  
        wxFrame.__init__(self, parent, -1, "Tv Inspector",
                             pos=wxDefaultPosition, 
                             size=wxDLG_SZE(parent, 300, 200))  
          
        parentApp.inspector = Filling(self, -1, rootObject={'tv': tv, 'app': parentApp}, rootLabel="Tv Luserland", rootIsNamespace=0)  
        self.parentApp = parentApp 
  
        wx.EVT_CLOSE(self, self.onCloseMe)  
  
    def onCloseMe(self, evt):  
        self.Show(0)  

