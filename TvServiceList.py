#!/bin/env python
#----------------------------------------------------------------------------
# Name:         TvServiceList.py
# Author:       XXXX
# Created:      XX/XX/XX
# Copyright:    
#----------------------------------------------------------------------------

__rcsid__ = "$Id: TvServiceList.py,v 1.2 2002/11/04 22:48:37 drt Exp $"

from wxPython.wx import *
from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin
import images

import tv.aggregator.db.services
from TvLuserland_wdr import *

class ListCtrlItemList:
    def __init__(self):
        self.datadict = {}
        self.servicelist = tv.aggregator.db.services.getsubscriptions()
        for x in tv.aggregator.db.services.getsubscriptions():
            self.add(x, tv.aggregator.db.services.getserviceflat(x))
        self.sortby("title") 

    def add(self, key, data):
        self.datadict[key] = data

    def sortby(self, sortby):
        sortlist = []
        for key, data in self.datadict.items():
            sortlist.append((data.get("sortby"), key))
        sortlist.sort()
        self.sortlist = sortlist
        
    def  __len__(self):
        """Called to implement the  built-in function
        len()  Returns the length   of  the object"""
        return len(self.datadict)

    def __getitem__(self, key):
        """Called to implement evaluation of
        self[key]."""
        return self.datadict[self.sortlist[key][1]]
    

# WDR: classes

class TestListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wxDefaultPosition,
                 size=wxDefaultSize, style=wxLC_REPORT|wxLC_VIRTUAL|wxSUNKEN_BORDER):#|wxLC_VRULES|wxLC_HRULES):
        wxListCtrl.__init__(self, parent, ID, pos, size, style)
        wxListCtrlAutoWidthMixin.__init__(self)
        self.columntitles = [("title", "Title"),
                             ("publicname", "Public Name"),
                             ("TVsourceurl", "URL")]
        self.columntokey = []

        pos = 0
        for key, title in self.columntitles:
            self.InsertColumn(pos, title)
            pos += 1
            self.columntokey.append(key)
        #self.SetColumnWidth(0, 175)
        #self.SetColumnWidth(1, 175)
        #self.SetColumnWidth(2, 175)
        
        self.itemlist = ListCtrlItemList()
        self.SetItemCount(len(self.itemlist))

        self.il = wxImageList(16, 16)
        self.idx1 = self.il.Add(images.getSmilesBitmap())
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())

        numColumns = self.GetColumnCount()
        self._colSortFlag = [0] * numColumns
        self._col = -1

        # WDR: handler declarations for ServiceList
        EVT_LIST_ITEM_ACTIVATED(self, self.GetId(), self.OnItemactivated)
        EVT_LIST_ITEM_SELECTED(self, self.GetId(), self.OnItemselected)
        EVT_LIST_DELETE_ALL_ITEMS(self, self.GetId(), self.OnDeleteallitems)
        EVT_LIST_DELETE_ITEM(self, self.GetId(), self.OnDeleteitem)
        EVT_LIST_END_LABEL_EDIT(self, self.GetId(), self.OnLabeledit)
        EVT_LIST_ITEM_RIGHT_CLICK(self, self.GetId(), self.OnItemrightclick)
        EVT_LIST_INSERT_ITEM(self, self.GetId(), self.OnInsertitem)
        EVT_LIST_ITEM_DESELECTED(self, self.GetId(), self.OnItemdeselected)
        EVT_LIST_COL_CLICK(self, self.GetId(), self.OnColClick)

        # for wxMSW
        #EVT_COMMAND_RIGHT_CLICK(self.list, tID, self.OnRightClick)
        # for wxGTK
        #EVT_RIGHT_UP(self.list, self.OnRightClick)
        #from pprint import pprint
        #pprint(dir(self))


    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calcualte them
    def OnGetItemText(self, item, col):
        self.itemlist
        return self.itemlist[item].get(self.columntokey[col])
    
    def OnGetItemImage(self, item):
        #if item % 3 == 0:
        #    return self.idx1
        #else:
        return -1
        
    def OnGetItemAttr(self, item):
        #if item % 3 == 1:
        #    return self.attr1
        #elif item % 3 == 2:
        #    return self.attr2
        #else:
        return None
                                

    # WDR: methods for ServiceList
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)


    def __updateImages(self, oldCol):
        sortImages = self.GetSortImages()
        if self._col != None and sortImages[0] != None:
            img = sortImages[self._colSortFlag[self._col]]
        if oldCol != None:
            self.ClearColumnImage(oldCol)
            self.SetColumnImage(self._col, img)

                                                                          
    # WDR: handler implementations for ServiceList



    def OnColClick(self, event):
        print "col click"
        oldCol = self._col
        self._col = col = event.GetColumn()
        self._colSortFlag[col] = not self._colSortFlag[col]
        self.GetListCtrl().SortItems(self.GetColumnSorter())
        self.__updateImages(oldCol)
        event.Skip()

    def OnItemactivated(self, event):
        print "activated"
        print self.itemlist[event.GetIndex()]
        import TvService
        dialog = TvService.ServiceDialog(self, self.itemlist[event.GetIndex()]["TVsourceurl"])
        dialog.Show()


    def OnItemselected(self, event):
        print "selected"
        event.Skip(true)        

    def OnItemdeselected(self, event):
        print "deselected"
        event.Skip(true)        

    def OnDeleteallitems(self, event):
        print "deletedall"
        event.Skip(true)

    def OnDeleteitem(self, event):
        print "deleted"
        event.Skip(true)

    def OnLabeledit(self, event):
        print "edited"
        event.Skip(true)

    def OnItemrightclick(self, event):
        print "rightclick"
        event.Skip(true)        

    def OnInsertitem(self, event):
        print "insert"
        event.Skip(true)        

class ServiceList(wxFrame, wxColumnSorterMixin):
    def __init__(self, parent):
        wxFrame.__init__(self, parent, -1, "XXX: Title", pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_FRAME_STYLE )

        #ServiceListFunc( self, true )
        #self.list = self.GetServicelist()
        self.list = TestListCtrl( self, -1 )
        
                                                     
        EVT_BUTTON(self, wxID_OK, self.OnOk)
        EVT_BUTTON(self, wxID_CANCEL, self.OnCancel)
        EVT_SIZE(self, self.OnSize)
        EVT_LIST_ITEM_ACTIVATED(self, ID_SERVICELIST, self.OnItemactivated)
        EVT_LIST_ITEM_SELECTED(self, ID_SERVICELIST, self.OnItemselected)
        EVT_LIST_DELETE_ALL_ITEMS(self, ID_SERVICELIST, self.OnDeleteallitems)
        EVT_LIST_DELETE_ITEM(self, ID_SERVICELIST, self.OnDeleteitem)
        EVT_LIST_END_LABEL_EDIT(self, ID_SERVICELIST, self.OnLabeledit)
        EVT_LIST_ITEM_RIGHT_CLICK(self, ID_SERVICELIST, self.OnItemrightclick)
        EVT_LIST_INSERT_ITEM(self, ID_SERVICELIST, self.OnInsertitem)

        # for wxMSW
        #EVT_COMMAND_RIGHT_CLICK(self.list, tID, self.OnRightClick)
        # for wxGTK
        #EVT_RIGHT_UP(self.list, self.OnRightClick)

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calcualte them
    def OnGetItemText(self, item, col):
        return "Item %d, column %d" % (item, col)
    
    def OnGetItemImage(self, item):
        #if item % 3 == 0:
        #    return self.idx1
        #else:
        return -1
        
    def OnGetItemAttr(self, item):
        #if item % 3 == 1:
        #    return self.attr1
        #elif item % 3 == 2:
        #    return self.attr2
        #else:
        return None
                                

    # WDR: methods for ServiceList

    def GetServicelist(self):
        return wxPyTypeCast( self.FindWindowById(ID_SERVICELIST), "wxListCtrl" )

    # WDR: handler implementations for ServiceList

    def OnItemactivated(self, event):
        print "activated"
        event.Skip(true)

    def OnItemselected(self, event):
        print "selected"
        event.Skip(true)        

    def OnDeleteallitems(self, event):
        print "deletedall"
        event.Skip(true)

    def OnDeleteitem(self, event):
        print "deleted"
        event.Skip(true)

    def OnLabeledit(self, event):
        print "edited"
        event.Skip(true)

    def OnItemrightclick(self, event):
        print "rightclick"
        event.Skip(true)        

    def OnInsertitem(self, event):
        print "insert"
        event.Skip(true)                

    def OnSize(self, event):
        event.Skip(true)

    def OnOk(self, event):
        event.Skip(true)

    def OnCancel(self, event):
        event.Skip(true)


