#!/bin/env python

__rcsid__ = "$Id: TvService.py,v 1.1 2002/11/01 08:55:10 drt Exp $"

from pprint import pformat

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
        self.GetLastnewitem().SetLabel(str(feedinfo.get("TVlastnewitem", "- unknown -")))
        self.GetItemsfetched().SetLabel(str(feedinfo.get("TVitemsfetched", "- unknown -")))
        self.GetLastrequest().SetLabel(str(feedinfo.get("TVlastfetched", "- unknown -")))
        self.GetChannelinfo().SetValue(pformat(feedinfo))
        self.GetPublicname().SetValue(config.get("publicname", ""))
        self.GetPrivatename().SetValue(feedinfo.get("privatename", ""))
        self.GetPubliclink().SetValue(feedinfo.get("publiclink", ""))
        #{         'TVetag': None,
        # 'description': ' (powered by http://www.newsisfree.com/syndicate.php - FOR PERSONAL AND NON COMMERCIAL USE ONLY!)',
        # 'language': 'en',
        # 'TVsourceurl': 'http://www.newsisfree.com/rss/60425ebaffc7cb6c5e746ed8c9181178/',
        # 'title': 'Powered by News Is Free',
        # 'TVmodified': (2002, 10, 29, 21, 7, 32, 1, 302, 0),
        # 'link': 'http://www.newsisfree.com/sources/info/1873/', 'TVcreated': <DateTime object for '2002-10-24 22:21:09.95' at 39d1520>,
        # 'date': '10/29/02 21:41 CET',
        #          'creator': 'mkrus@newsisfree.com'}
        
        # WDR: handler declarations for ServiceDialog
        EVT_BUTTON(self, ID_REMOVESERVICE, self.OnRemove)
        EVT_BUTTON(self, wxID_OK, self.OnOk)
        EVT_IDLE(self, self.OnIdle)

    # WDR: methods for ServiceDialog

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

    def Validate(self, win):
        return true

    # WDR: handler implementations for ServiceDialog

    def OnRemove(self, event):
        tv.aggregator.db.services.unsubscribe(self.serviceurl)
        self.OnOk(event)
        
    def OnIdle(self, event):
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
        #config["fetchhowoften"]
        tv.aggregator.db.services.saveconfig(self.serviceurl, config)

        #howoften = self.GetHowoften().GetString()
        howoften = self.GetHowoften().GetStringSelection()
        print howoften, config["publiclink"], config["publicname"], config["privatename"]
        self.Show(FALSE)



