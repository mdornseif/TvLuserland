__rcsid__ = "$Id: TvNewsPane.py,v 1.10 2002/11/14 15:48:45 drt Exp $"

from wxPython.wx import *
from wxPython.html import *

from TvNewsEditor import *
from TvService import *

from TvLuserland_wdr import *

import tv.config
import tv.aggregator.db.items
import tv.aggregator.db.services

_items = tv.aggregator.db.items.getitemsByDate(maxitems=tv.config.get('ui.newsitems'))

from pprint import pprint

# WDR: classes

def inspect(object):
    probes = [
              'GetAutoLayout', 'GetBackgroundColour', 'GetBestSize',
              'GetBorder', 'GetCaret', 'GetCharHeight',
              'GetCharWidth', 'GetClassName', 'GetClientAreaOrigin',
              'GetClientRect', 'GetClientSize', 'GetClientSizeTuple',
              'GetConstraints', 'GetContainingSizer', 'GetCursor',
              'GetDefaultItem', 'GetDropTarget', 'GetEventHandler',
              'GetEvtHandlerEnabled', 'GetFont',
              'GetForegroundColour', 'GetGrandParent', 'GetHandle',
              'GetHelpText', 'GetId', 'GetLabel', 'GetMaxSize',
              'GetMinSize', 'GetMinSizeTuple', 'GetName',
              'GetNextHandler', 'GetOrientation', 'GetParent',
              'GetPosition', 'GetPositionTuple', 'GetRect',
              'GetScaleX', 'GetScaleY', 'GetScrollPageSize',
              'GetScrollPixelsPerUnit', 'GetScrollPos',
              'GetScrollRange', 'GetScrollThumb', 'GetSize',
              'GetSizeTuple', 'GetSizer', 'GetTargetWindow',
              'GetTextExtent', 'GetTitle', 'GetToolTip',
              'GetUpdateRegion', 'GetValidator', 'GetViewStart',
              'GetVirtualSize', 'GetVirtualSizeTuple',
              'GetWindowStyleFlag', 'HasCapture', 'HasScrollbar',
              'HitTest', 'InitDialog', 'IsBeingDeleted', 'IsEnabled',
              'IsExposed', 'IsExposedPoint', 'IsExposedRect',
              'IsRetained', 'IsShown', 'IsTopLevel'
              ]
    
class NewsItem(wxPanel):
    def __init__(self, parent, item, id = -1, pos = wxPyDefaultPosition,
                 size=wxPyDefaultSize, style=wxSUNKEN_BORDER):
        wxPanel.__init__(self, parent, id, pos, size, style)
        
        self.item = item
        self.parent = parent

        # test wxPyClickableHtmlWindow and wxGenStaticText
        self.html = wxHtmlWindow(self, -1, size=wxDLG_SZE(self, 300, -1),
                                 style=wxHW_SCROLLBAR_NEVER)
        self.html.SetPage("<html><body>%s</body></html>" % item.get("description", "-no description-"))
        ir = self.html.GetInternalRepresentation()
        self.html.SetSize( (min(800, ir.GetWidth()+5), ir.GetHeight()+5))
        wdr = NewsItemFunc( self, true )
        self.SetLabelAndResize(self.GetTitle(), item.get("title", ""))
        self.GetLink().SetLabel(item.get("link", ""))
        self.SetLabelAndResize(self.GetDate(), str(item.get("TVdateobject", ""))[:-3])
        self.GetSource().SetLabel(tv.aggregator.db.services.getconfig(item["TVsourceurl"]).get("privatename", ""))
 
        # WDR: handler declarations for NewsItem
        EVT_BUTTON(self, ID_SOURCE, self.OnSource)
        EVT_BUTTON(self, ID_EDIT, self.OnEdit)
        EVT_BUTTON(self, ID_KILL, self.OnKill)
        EVT_BUTTON(self, ID_SOURCE, self.OnSource)
        EVT_SIZE(self, self.OnSize)

    def SetLabelAndResize(self, control, label):
        control.SetLabel(str(label))
        control.SetSize(control.GetBestSize())
        control.GetContainingSizer().SetItemMinSize(control,
                                                 control.GetSize().GetWidth(),
                                                 control.GetSize().GetHeight())
        control.GetContainingSizer().Layout()

    
    # WDR: methods for NewsItem

    def GetDate(self):
        return wxPyTypeCast( self.FindWindowById(ID_DATE), "wxStaticText" )

    def GetLink(self):
        return self.FindWindowById(ID_LINK)
        #return wxPyTypeCast( self.FindWindowById(ID_LINK), "wxStaticText" )

    def GetTitle(self):
        return wxPyTypeCast( self.FindWindowById(ID_TITLE), "wxStaticText" )

    def GetSource(self):
        return self.FindWindowById(ID_SOURCE)
        #return wxPyTypeCast( self.FindWindowById(ID_SOURCE), "wxStaticText" )

    def GetHtml(self):
        return wxPyTypeCast( self.FindWindowById(ID_HTML), "wxHtmlWindow" )

    def GetEdit(self):
        return wxPyTypeCast( self.FindWindowById(ID_EDIT), "wxButton" )

    def GetPost(self):
        return wxPyTypeCast( self.FindWindowById(ID_POST), "wxButton" )

    def GetKill(self):
        return wxPyTypeCast( self.FindWindowById(ID_KILL), "wxButton" )

    # WDR: handler implementations for NewsItem

    def OnSource(self, event):
        dialog = ServiceDialog(self.parent, self.item.get("TVsourceurl"))
        dialog.Show()

    def OnEdit(self, event):
        dialog = EditPostDialog(self.parent, -1, item = self.item, killfunc = lambda: self.parent.removeItem(self.GetId(), self.item))
        dialog.Show()

    def OnKill(self, event):
        self.parent.removeItem(self.GetId(), self.item)
        self.Destroy()

    def OnSize(self, event):
        # XXX
        #wxPanel.OnSize(self, event)
        event.Skip()


class TvNewsPane(wxScrolledWindow):
    def __init__(self, parent):
        wxScrolledWindow.__init__(self, parent, -1,
                                  style = wxTAB_TRAVERSAL|wxSIMPLE_BORDER)


        from pprint import pprint
        # XXX: a weak reference might be better
        self.displayed_items = []
        #self.panel = wxPanel(self, -1)
        self.sizer = self.createContentBox()
        self.SetAutoLayout( true )
        self.SetSizer(self.sizer)
        #self.sizer.Fit( self )
        #self.sizer.SetSizeHints( self )
         
        # The following is all that is needed to integrate the sizer and the
        # scrolled window.  In this case we will only support vertical scrolling.
        self.EnableScrolling(false, true)
        self.SetScrollRate(0, 20)
        self.sizer.SetVirtualSizeHints(self)
        #EVT_CHILD_FOCUS(self, self.OnChildFocus)
        self.SetSize((660, 400))
        self.fixlayout()
        wxCallAfter(self.Scroll, 0, 0) # scroll back to top after initial events

    def createContentBox(self):
        box = wxBoxSizer(wxVERTICAL)        
        for item in _items:
            x = self.createItemBox(item)
            box.Add(x, 0, wxGROW)
            self.displayed_items.append(x)
        box.Add(5, 5)
        return box
        
    def createItemBox(self, item):
        if 'itemBox' not in item:
            item['itemBox'] = NewsItem(self, item)
        return item['itemBox']

    def removeItem(self, cId, item):
        """Remove a item from the newspane and the database.

        Needs the wxID of the Newsitem and the item itself"""
        # XXX better give more data to deleteitem
        # remove from db
        tv.aggregator.db.items.deleteitem(item['guid'])
        # remove window
        self.sizer.Remove(self.FindWindowById(cId))
        self.fixlayout()
        
    def removeAllItems(self):
        # XXX: fix me
        for x in self.displayed_items:
            print x.GetId()
            print x.item

    def fixlayout(self):
        w, h = self.sizer.GetMinSize()
        self.SetVirtualSizeHints(w, h)
        #self.sizer.Layout()
        self.Layout()
        self.Refresh()
        self.AdjustScrollbars()
        
                     
