__rcsid__ = "$Id: TvNewsPane.py,v 1.3 2002/10/31 22:35:09 drt Exp $"

from wxPython.wx import *
from wxPython.html import *

from TvNewsEditor import *
from TvService import *

from TvLuserland_wdr import *

import tv.aggregator.db.items
import tv.aggregator.db.services

_items = tv.aggregator.db.items.getitemsByDate(maxitems=20)

from pprint import pprint

# WDR: classes

class NewsItem(wxPanel):
    def __init__(self, parent, item, id = -1, pos = wxPyDefaultPosition,
                 size=wxPyDefaultSize, style=wxSUNKEN_BORDER):
        wxPanel.__init__(self, parent, id, pos, size, style)
        
        self.item = item
        self.parent = parent

        # test wxPyClickableHtmlWindow and wxGenStaticText
        self.html = wxHtmlWindow(self, -1, size=wxDLG_SZE(self, 300, -1),
                                 style=wxHW_SCROLLBAR_NEVER)
        self.html.SetPage("<html><body>%s</body></html>" % self.create_html(item))
        ir = self.html.GetInternalRepresentation()
        self.html.SetSize( (ir.GetWidth()+5, ir.GetHeight()+5))
        wdr = NewsItemFunc( self, true )
        source = self.GetSource()
        source.SetLabel(tv.aggregator.db.services.getconfig(item["TVsourceurl"]).get("privatename", ""))

        # WDR: handler declarations for NewsItem
        EVT_BUTTON(self, ID_EDIT, self.OnEdit)
        EVT_BUTTON(self, ID_POST, self.OnPost)
        EVT_BUTTON(self, ID_KILL, self.OnKill)
        EVT_BUTTON(self, ID_SOURCE, self.OnSource)
        EVT_LEFT_UP(self.GetSource(), self.OnSource)
                

    def create_html(self, item):
        return "<b>%s</b><br><i>%s</i><br>%s" % (item.get("title", "").strip(),
                                             item.get("link", "").strip()[:50],
                                             item.get("description"))
    
    # WDR: methods for NewsItem
    def GetSource(self):
        return self.FindWindowById(ID_SOURCE)
        return wxPyTypeCast( self.FindWindowById(ID_SOURCE), "wxStaticText" )

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

    def OnPost(self, event):
        print "POST --- nada!"

    def OnKill(self, event):
        self.parent.removeItem(self.GetId(), self.item)
        self.Destroy()


class TvNewsPane(wxScrolledWindow):
    def __init__(self, parent):
        wxScrolledWindow.__init__(self, parent, -1,
                                  style = wxTAB_TRAVERSAL|wxSIMPLE_BORDER)
        
        self.displayed_items = []
        self.sizer = self.createContentBox()
        self.SetSizer(self.sizer)
        
        # The following is all that is needed to integrate the sizer and the
        # scrolled window.  In this case we will only support vertical scrolling.
        self.EnableScrolling(false, true)
        self.SetScrollRate(0, 20)
        self.sizer.SetVirtualSizeHints(self)
        EVT_CHILD_FOCUS(self, self.OnChildFocus)
        self.SetSize((660, 400))
        wxCallAfter(self.Scroll, 0, 0) # scroll back to top after initial events

    def createContentBox(self):
        box = wxBoxSizer(wxVERTICAL)        
        for item in _items:
            x = self.createItemBox(item)
            box.Add(x)
            self.displayed_items.append(x)
        box.Add(5, 5)
        return box
        
    def createItemBox(self, item):
        if 'itemBox' not in item:
            item['itemBox'] = NewsItem(self, item)
        return item['itemBox']

    def removeItem(self, cId, item):
        # XXX better give more data to deleteitem
        tv.aggregator.db.items.deleteitem(item['guid'])
        self.sizer.Remove(self.FindWindowById(cId))
        self.sizer.Layout()
        self.Layout()
        self.Refresh()
        self.AdjustScrollbars()
        self.refresh()
        #wxCallAfter(self.Scroll, 0, 0) # scroll back to top after initial events
        # XXX resize

    def refresh(self):
        _items = tv.aggregator.db.items.getitemsByDate(maxitems=100)
        print "XXX: refreshing"

    def OnChildFocus(self, evt):
        # If the child window that gets the focus is not visible,
        # this handler will try to scroll enough to see it.  If you
        # need to handle horizontal auto-scrolling too then this will
        # need adapted.
        evt.Skip()
        child = evt.GetWindow()

        sppu_y = self.GetScrollPixelsPerUnit()[1]
        vs_y   = self.GetViewStart()[1]
        cpos = child.GetPosition()
        csz  = child.GetSize()

        # is it above the top?
        if cpos.y < 0:
            new_vs = cpos.y / sppu_y
            self.Scroll(-1, new_vs)

        # is it below the bottom ?
        if cpos.y + csz.height > self.GetClientSize().height:
            diff = (cpos.y + csz.height - self.GetClientSize().height) / sppu_y
            self.Scroll(-1, vs_y + diff + 1)
