#!/bin/env python

__rcsid__ = "$Id: TvService.py,v 1.4 2002/11/05 10:49:02 drt Exp $"

from pprint import pformat
import time

from wxPython.wx import *
from TvLuserland_wdr import *

import tv.aggregator.db.services

# WDR: classes

class ServiceDialog(wxDialog):
    def __init__(self, parent, serviceurl):
        wxDialog.__init__(self, parent, -1, "XXX: title", pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_DIALOG_STYLE)
        
        self.serviceurl = serviceurl
        ServiceDialogFunc( self, true )
        service = tv.aggregator.db.services.getservice(serviceurl)
        feedinfo = service["feedinfo"]
        config = service["config"]
        self.SetLabelAndResize(self.GetTitle(), feedinfo.get("title", "- unknown -"))
        self.GetLink().SetLabel(str(feedinfo.get("link", "- unknown -")))
        self.GetPublicname().SetValue(config.get("publicname", feedinfo.get("title", "")))
        self.GetPrivatename().SetValue(config.get("privatename", config.get("publicname", feedinfo.get("title", ""))))
        self.GetPubliclink().SetValue(config.get("publiclink", feedinfo.get("link", "")))
        howoften = config.get("fetchhowoften", 60)
        if howoften / 60  >= 1:
            howoften = "%dh" % int(howoften/60)
        else:
            howoften = "%dm" % howoften
        self.GetHowoften().SetStringSelection(howoften)
        self.GetCheckforredirected().SetValue(config.get("checkforredirected", 0))
        self.GetRemovemarkup().SetValue(config.get("removemarkup", 0))
        self.GetExtractltd().SetValue(config.get("extractid", 0))
        self.GetFixumlauts().SetValue(config.get("fixumlauts", 0))
        
        
        self.UpdateFeedinfo()
        
        # WDR: handler declarations for ServiceDialog
        EVT_BUTTON(self, ID_KILLITEMS, self.OnKillitems)
        EVT_BUTTON(self, ID_REMOVESERVICE, self.OnRemove)
        EVT_BUTTON(self, wxID_OK, self.OnOk)
        EVT_IDLE(self, self.OnIdle)

    # WDR: methods for ServiceDialog

    def GetLink(self):
        return self.FindWindowById(ID_LINK)
        # return wxPyTypeCast( self.FindWindowById(ID_LINK), "wxStaticText" )

    def GetTitle(self):
        return wxPyTypeCast( self.FindWindowById(ID_TITLE), "wxStaticText" )

    def GetHowoften(self):
        return wxPyTypeCast( self.FindWindowById(ID_HOWOFTEN), "wxChoice" )

    def GetRemovemarkup(self):
        return wxPyTypeCast( self.FindWindowById(ID_REMOVEMARKUP), "wxCheckBox" )

    def GetExtractltd(self):
        return wxPyTypeCast( self.FindWindowById(ID_EXTRACTLTD), "wxCheckBox" )

    def GetFixumlauts(self):
        return wxPyTypeCast( self.FindWindowById(ID_FIXUMLAUTS), "wxCheckBox" )

    def GetCheckforredirected(self):
        return wxPyTypeCast( self.FindWindowById(ID_CHECKFORREDIRECTED), "wxCheckBox" )

    def GetPrivatename(self):
        return wxPyTypeCast( self.FindWindowById(ID_PRIVATENAME), "wxTextCtrl" )

    def GetPublicname(self):
        return wxPyTypeCast( self.FindWindowById(ID_PUBLICNAME), "wxTextCtrl" )

    def GetPubliclink(self):
        return wxPyTypeCast( self.FindWindowById(ID_PUBLICLINK), "wxTextCtrl" )

    def GetChannelinfo(self):
        return wxPyTypeCast( self.FindWindowById(ID_CHANNELINFO), "wxTextCtrl" )

    def GetUnreaditems(self):
        return wxPyTypeCast( self.FindWindowById(ID_UNREADITEMS), "wxStaticText" )

    def GetLasterrortext(self):
        return wxPyTypeCast( self.FindWindowById(ID_LASTERRORTEXT), "wxStaticText" )

    def GetLasterror(self):
        return wxPyTypeCast( self.FindWindowById(ID_LASTERROR), "wxStaticText" )

    def GetErrors(self):
        return wxPyTypeCast( self.FindWindowById(ID_ERRORS), "wxStaticText" )

    def GetLastnewitem(self):
        return wxPyTypeCast( self.FindWindowById(ID_LASTNEWITEM), "wxStaticText" )

    def GetItemsfetched(self):
        return wxPyTypeCast( self.FindWindowById(ID_ITEMSFETCHED), "wxStaticText" )

    def GetLastrequest(self):
        return wxPyTypeCast( self.FindWindowById(ID_LASTREQUEST), "wxStaticText" )

    def SetLabelAndResize(self, control, label):
        control.SetLabel(str(label))
        control.SetSize(control.GetBestSize())
        control.GetContainingSizer().SetItemMinSize(control,
                                                 control.GetSize().GetWidth(),
                                                 control.GetSize().GetHeight())
        control.GetContainingSizer().Layout()

    def UpdateFeedinfo(self):
        feedinfo = tv.aggregator.db.services.getfeedinfo(self.serviceurl)
        self.SetLabelAndResize(self.GetLastnewitem(), feedinfo.get("TVlastnewitem", "- unknown -"))
        self.SetLabelAndResize(self.GetItemsfetched(), feedinfo.get("TVitemsfetched", "- unknown -"))
        self.SetLabelAndResize(self.GetLastrequest(), feedinfo.get("TVlastfetched", "- unknown -"))
        self.SetLabelAndResize(self.GetErrors(), feedinfo.get("TVerrors", "- unknown -"))
        self.SetLabelAndResize(self.GetLasterror(), feedinfo.get("TVlasterror", "- unknown -"))
        self.SetLabelAndResize(self.GetLasterrortext(), feedinfo.get("TVlasterrortext", "- unknown -"))
        cleanFeedinfo = {}
        for k, v in feedinfo.items():
            if not k.startswith("TV"):
                cleanFeedinfo[k] = v
        self.GetChannelinfo().SetValue("%r =\n%s" % (self.serviceurl, pformat(cleanFeedinfo)))
        self.SetLabelAndResize(self.GetUnreaditems(), tv.aggregator.db.items.getnrofunreaditemsforsource(self.serviceurl))
        self._lastupdate = time.time()

    # WDR: handler implementations for ServiceDialog

    def OnKillitems(self, event):
        tv.aggregator.db.items.deleteallitemsfromsource(self.serviceurl)
        self.UpdateFeedinfo()
        # XXX: inform newspane

    def OnRemove(self, event):
        tv.aggregator.db.services.unsubscribe(self.serviceurl)
        self.OnOk(event)
    
    def OnIdle(self, event):
        if self._lastupdate + 10 < time.time():
            self.UpdateFeedinfo()            
        event.Skip(true)

    def OnOk(self, event):
        service = tv.aggregator.db.services.getservice(self.serviceurl)
        feedinfo = service["feedinfo"]
        config = service["config"]
        config["publicname"] = self.GetPublicname().GetValue().strip()
        config["privatename"] = self.GetPrivatename().GetValue().strip()
        config["publiclink"] = self.GetPubliclink().GetValue().strip()
        if config["publiclink"] == "":
            config["publiclink"] = service.get("link", "")
        if config["publicname"] == "" and config["privatename"] != "":
            config["publicname"] = config["privatename"]
        if config["privatename"] == "" and config["publicname"] != "":
            config["privatename"] = config["publicname"]
        howoften = self.GetHowoften().GetStringSelection()
        if howoften.endswith('m'):
            config["fetchhowoften"] = int(howoften[:-1])
        elif howoften.endswith('h'):
            config["fetchhowoften"] = int(howoften[:-1]) * 60
        else:
          print "unknown choice"
        config["checkforredirected"] = self.GetCheckforredirected().GetValue()
        config["removemarkup"] = self.GetRemovemarkup().GetValue()
        config["extractid"] = self.GetExtractltd().GetValue()
        config["fixumlauts"] = self.GetFixumlauts().GetValue()

        tv.aggregator.db.services.saveconfig(self.serviceurl, config)

        print howoften, config["publiclink"], config["publicname"], config["privatename"]
        self.Show(FALSE)
        self.Destroy()


