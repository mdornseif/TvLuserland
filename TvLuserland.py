#!/usr/local/bin/python
#----------------------------------------------------------------------------
# Name:         TvLuserland.py
# Author:       md@hudora.de
# Created:      13/10/2002
# Copyright:    nope
#----------------------------------------------------------------------------

__rcsid__ = "$Id: TvLuserland.py,v 1.5 2002/11/04 22:40:28 drt Exp $"

from wxPython.wx import *
from wxPython.html import *

from TvLuserland_wdr import *

from TvNewsPane import *
from TvNewsEditor import *

from pprint import pprint

import tv.aggregator.db.services

class TvMainFrame(wxFrame):
    def __init__(self, parent, id, title,
        pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_FRAME_STYLE ):
        wxFrame.__init__(self, parent, id, title, pos, size, style)
        
        if wxPlatform == "__WXMAC__":
            wxApp.s_macAboutMenuItemId = wxID_ABOUT
        #self.SetAppName("tv")
        #SetVendorName()
        # On Mac OS X, the Preferences item goes in a special place, too.
        # A similar variable will be added to wxMac shortly - check the <wx/app.h> header file.

        self.CreateMyMenuBar()
        
        self.CreateMyToolBar()
        
        self.CreateStatusBar(1)
        self.SetStatusText("Starting")
        
        self.newspane = TvNewsPane(self)

        # insert main window here
        ReadNewsFunc(self)

        # examples
        #t = self.GetServicetree()
        #r = t.AddRoot("Root")
        #t.SetPyData(r, None)
        #c = t.AppendItem(r, "Alle Services")
        #t.SetPyData(c, None)
        #c = t.AppendItem(r, "Services nach Name")
        #t.SetPyData(c, None)
        #c = t.AppendItem(r, "Services nach URL")
        #t.SetPyData(c, None)
        #for x in tv.aggregator.db.services.getsubscriptions():
        #    t.AppendItem(c, x)
        #c = t.AppendItem(r, "Sonstwas")
        #t.SetPyData(c, None)

        # WDR: handler declarations for TvMainFrame
        EVT_BUTTON(self, ID_NEWSERVICE, self.OnNewservice)
        EVT_BUTTON(self, ID_SERVICELIST, self.OnServicelist)
        EVT_BUTTON(self, ID_REFRESH, self.OnRefresh)
        EVT_BUTTON(self, ID_NEWPOST, self.OnNewpost)
        EVT_MENU(self, wxID_ABOUT, self.OnAbout)
        EVT_MENU(self, ID_PREFERENCES, self.OnPreferences)
        EVT_MENU(self, ID_QUIT, self.OnQuit)
        EVT_CLOSE(self, self.OnCloseWindow)
        

    # WDR: methods for TvMainFrame
    
    def GetServicelist(self):
        return wxPyTypeCast( self.FindWindowById(ID_SERVICELIST), "wxButton" )

    def GetNewservice(self):
        return wxPyTypeCast( self.FindWindowById(ID_NEWSERVICE), "wxButton" )

    def GetItemscroller(self):
        return wxPyTypeCast( self.FindWindowById(ID_NEWSPANE), "wxScrolledWindow" )

    def GetServicetree(self):
        window = self.FindWindowById(ID_SERVICETREE)
        if hasattr(window, "this"):
            newPtr = ptrcast(window.this, "wxPyTreeCtrl_p")
        else:
            newPtr = ptrcast(window, "wxPyTreeCtrl_p")
        theClass = globals()["wxTreeCtrlPtr"]
        theObj = theClass(newPtr)
        if hasattr(window, "this"):
            theObj.thisown = window.thisown
        return theObj

    def CreateMyMenuBar(self):
        file_menu = wxMenu()
        help_menu = wxMenu()
        help_menu.Append(wxID_ABOUT, "About...", "Program info")
        file_menu.Append(ID_PREFERENCES, "Preferences", "Preferences and Configuration")
        file_menu.Append(ID_QUIT, "Quit...", "Quit program")
        
        menu_bar = wxMenuBar()
        menu_bar.Append(file_menu, "File")
        #menu_bar.Append(help_menu, "&Help")
        
        self.SetMenuBar(menu_bar)
    
    def CreateMyToolBar(self):
        tb = self.CreateToolBar(wxTB_HORIZONTAL|wxNO_BORDER)
        
        # tb.AddSimpleTool( ID_QUIT, wxNoRefBitmap(...,wxBITMAP_TYPE_PNG), "Quit" )
        
        tb.Realize()
    
    # WDR: handler implementations for TvMainFrame
    
    def OnNewservice(self, event):
        import TvNewService
        TvNewService.NewService(self)
        

    def OnServicelist(self, event):
        import TvServiceList
        dialog = TvServiceList.ServiceList(self)
        dialog.CentreOnParent()
        dialog.Show()
        

    def OnRefresh(self, event):
        self.GetItemscroller().refresh()

    def OnNewpost(self, event):
        # user is requesting new posting form
        dialog = EditPostDialog(self, -1)
        dialog.Show()
        
    def OnPreferences(self, event):
        import TvConfig 
        dialog = TvConfig.ConfigDialog(self, -1)
        dialog.CentreOnParent()
        dialog.ShowModal()
        dialog.Destroy()

    def OnAbout(self, event):
        dialog = wxMessageDialog(self, "This is TV Luserland - work in Progress\nhackers@c0re.jp",
            "About TV Luserland", wxOK|wxICON_INFORMATION )
        dialog.CentreOnParent()
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnQuit(self, event):
        self.Close(true)
    
    def OnCloseWindow(self, event):
        self.Destroy()


#----------------------------------------------------------------------------

class TvApp(wxApp):
    
    def OnInit(self):
        wxInitAllImageHandlers()
        frame = TvMainFrame(None, -1, "TV Luserland", wxPoint(20,20), wxSize(500,340) )
        frame.Show(true)
        
        return true

#----------------------------------------------------------------------------

app = TvApp(0)
app.MainLoop()

