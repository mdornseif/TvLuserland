from wxPython.wx import *
from wxPython.html import *

from TvLuserland_wdr import *

import tv.config


class ConfigDialog(wxDialog):
    def __init__(self, parent, id,
        pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_DIALOG_STYLE ):
        wxDialog.__init__(self, parent, id, "Configuration", pos, size, style)
        
        ConfigFunc( self, true )
        
        # WDR: handler declarations for TvConfig
        EVT_BUTTON(self, ID_CWLOGAUTODETECT, self.OnlogAutodetect)
        EVT_BUTTON(self, wxID_OK, self.OnOk)
        EVT_BUTTON(self, wxID_CANCEL, self.OnCancel)

        # dos this work?
        self.GetCwlogpassword().SetWindowStyleFlag(wxTE_PASSWORD)
        self.GetCwlogpassword().Refresh()

        # set initial values
        self.GetCuiitems().SetValue(tv.config.get('ui.newsitems'))
        self.GetCuidelafterpost().SetValue(tv.config.get('ui.deleteafterpost'))
        self.GetCuiautopreview().SetValue(tv.config.get('ui.autopreview'))
        self.GetCwlogserver().SetValue(tv.config.get('weblog.server'))
        self.GetCwlogmetaapi().SetValue(tv.config.get('weblog.hasMetaWeblogApi'))
        self.GetCwlogsetdate().SetValue(tv.config.get('weblog.hasSetDate'))
        self.GetCwlogaggregator().SetValue(tv.config.get('weblog.hasAggregatorApi'))
        self.GetCwlogdebug().SetValue(tv.config.get('weblog.xmlrpcdebug'))
        self.GetCwloguser().SetValue(tv.config.get('weblog.user'))
        self.GetCwlogpassword().SetValue(tv.config.get('weblog.password'))
        self.GetCnettimeout().SetValue(tv.config.get('net.timeout'))
        self.GetCfsdbdir().SetValue(tv.config.get('fs.dbdir'))
        
    # WDR: methods for TvConfig

    def GetCnettimeout(self):
        return wxPyTypeCast( self.FindWindowById(ID_CNETTIMEOUT), "wxSpinCtrl" )

    def GetCfsdbdir(self):
        return wxPyTypeCast( self.FindWindowById(ID_CFSDBDIR), "wxTextCtrl" )

    def GetCwlogdebug(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGDEBUG), "wxCheckBox" )

    def GetCwlogpassword(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGPASSWORD), "wxTextCtrl" )

    def GetCwloguser(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGUSER), "wxTextCtrl" )

    def GetCuiitems(self):
        return wxPyTypeCast( self.FindWindowById(ID_CUIITEMS), "wxSpinCtrl" )

    def GetCuidelafterpost(self):
        return wxPyTypeCast( self.FindWindowById(ID_CUIDELAFTERPOST), "wxCheckBox" )

    def GetCuiautopreview(self):
        return wxPyTypeCast( self.FindWindowById(ID_CUIAUTOPREVIEW), "wxCheckBox" )

    def GetCwlogaggregator(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGAGGREGATOR), "wxCheckBox" )

    def GetCwlogsetdate(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGSETDATE), "wxCheckBox" )

    def GetCwlogmetaapi(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGMETAAPI), "wxCheckBox" )

    def GetCwlogserver(self):
        return wxPyTypeCast( self.FindWindowById(ID_CWLOGSERVER), "wxTextCtrl" )

    # WDR: handler implementations for TvConfig

    def OnlogAutodetect(self, event):
        event.Skip(true)

    def OnOk(self, event):
        tv.config.set('ui.newsitems', self.GetCuiitems().GetValue())
        tv.config.set('ui.deleteafterpost', self.GetCuidelafterpost().GetValue())
        tv.config.set('ui.autopreview', self.GetCuiautopreview().GetValue())
        tv.config.set('weblog.server', self.GetCwlogserver().GetValue())
        tv.config.set('weblog.hasMetaWeblogApi', self.GetCwlogmetaapi().GetValue())
        tv.config.set('weblog.hasSetDate', self.GetCwlogsetdate().GetValue())
        tv.config.set('weblog.hasAggregatorApi', self.GetCwlogaggregator().GetValue())
        tv.config.set('weblog.xmlrpcdebug', self.GetCwlogdebug().GetValue())
        tv.config.set('weblog.user', self.GetCwloguser().GetValue())
        tv.config.set('weblog.password', self.GetCwlogpassword().GetValue())
        tv.config.set('net.timeout', self.GetCnettimeout().GetValue())
        tv.config.set('fs.dbdir', self.GetCfsdbdir().GetValue())
        tv.config.save()
        event.Skip(true)

    def OnCancel(self, event):
        event.Skip(true)

