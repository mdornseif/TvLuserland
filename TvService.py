#!/bin/env python

__rcsid__ = "$Id: TvService.py,v 1.5 2002/12/23 18:58:58 drt Exp $"

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
        feedinfo, feedconfig = tv.aggregator.db.services.getserviceinfoandconfig(serviceurl)
        self.SetLabelAndResize(self.GetTitle(), feedinfo.get("title", "- unknown -"))
        self.GetLink().SetLabel(str(feedinfo.get("link", "- unknown -")))
        self.GetPublicname().SetValue(feedconfig.get("publicname", feedinfo.get("title", "")))
        self.GetPrivatename().SetValue(feedconfig.get("privatename", feedconfig.get("publicname", feedinfo.get("title", ""))))
        self.GetPubliclink().SetValue(feedconfig.get("publiclink", feedinfo.get("link", "")))
        howoften = feedconfig.get("fetchhowoften", 60)
        if howoften / 60  >= 1:
            howoften = "%dh" % int(howoften/60)
        else:
            howoften = "%dm" % howoften
        self.GetHowoften().SetStringSelection(howoften)
        self.GetCheckforredirected().SetValue(feedconfig.get("checkforredirected", 0))
        self.GetRemovemarkup().SetValue(feedconfig.get("removemarkup", 0))
        self.GetExtractltd().SetValue(feedconfig.get("extractid", 0))
        self.GetFixumlauts().SetValue(feedconfig.get("fixumlauts", 0))
        
        
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
        feedinfo, feedconfig = tv.aggregator.db.services.getserviceinfoandconfig(self.serviceurl)
        feedconfig["publicname"] = self.GetPublicname().GetValue().strip()
        feedconfig["privatename"] = self.GetPrivatename().GetValue().strip()
        feedconfig["publiclink"] = self.GetPubliclink().GetValue().strip()
        if feedconfig["publiclink"] == "":
            feedconfig["publiclink"] = service.get("link", "")
        if feedconfig["publicname"] == "" and feedconfig["privatename"] != "":
            feedconfig["publicname"] = feedconfig["privatename"]
        if feedconfig["privatename"] == "" and feedconfig["publicname"] != "":
            feedconfig["privatename"] = feedconfig["publicname"]
        howoften = self.GetHowoften().GetStringSelection()
        if howoften.endswith('m'):
            feedconfig["fetchhowoften"] = int(howoften[:-1])
        elif howoften.endswith('h'):
            feedconfig["fetchhowoften"] = int(howoften[:-1]) * 60
        else:
          print "unknown choice"
        feedconfig["checkforredirected"] = self.GetCheckforredirected().GetValue()
        feedconfig["removemarkup"] = self.GetRemovemarkup().GetValue()
        feedconfig["extractid"] = self.GetExtractltd().GetValue()
        feedconfig["fixumlauts"] = self.GetFixumlauts().GetValue()

        tv.aggregator.db.services.savefeedconfig(self.serviceurl, feedconfig)

        print howoften, feedconfig["publiclink"], feedconfig["publicname"], feedconfig["privatename"]
        self.Show(FALSE)
        self.Destroy()


