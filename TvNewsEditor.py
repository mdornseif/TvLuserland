from wxPython.wx import *
from wxPython.html import *
if wxPlatform == "__WXMSW__":
    from wxPython.iewin import *

from TvLuserland_wdr import *

import tv.weblog.metaWeblog
import tv.aggregator.db.services
import tv.weblog.tools

from asyncfunccall import *

import urllib
import mx.DateTime

# category cache
catnames = None

# constants

ID_QUIT = 100

# WDR: classes
  
class EditPostDialog(wxDialog):
    def __init__(self, parent, id, title = None,
        pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_DIALOG_STYLE | wxRESIZE_BORDER, item = {}, killfunc = None ):
        global catnames

        self.item = item
        self.killfunc = killfunc
        self.targetdate = None
        if title == None:
            title = "Posting: %s" % (item.get("title", ""))

        wxDialog.__init__(self, parent, id, title, pos, size, style)
        
        DialogElements = EditPostFunc( self, true )
                                                                
        # preset content if wanted
        self.GetPosttitle().SetValue(item.get("title", "").strip())
        self.GetPostlink().SetValue(item.get("link", "").strip())


        # XXX: configurable
        if mx.DateTime.now() > item.get("TVdateobject", mx.DateTime.now())  + mx.DateTime.TimeDelta(4*24):
            print "now:", mx.DateTime.now(), "delta:", mx.DateTime.TimeDelta(3)
            print "object:", item.get("TVdateobject", mx.DateTime.now()), "added:", item.get("TVdateobject", mx.DateTime.now())  + mx.DateTime.TimeDelta(3)
            self.GetDate().SetLabel(item.get("TVdateobject", mx.DateTime.now()).strftime("%e. %B %Y (%D)"))
            self.targetdate = item.get("TVdateobject", mx.DateTime.now())
        else:
            self.GetDate().SetLabel("unchanged - %s" % item.get("TVdateobject", mx.DateTime.now()).strftime("%e. %B %Y (%D)"))

        if "author" in item:
            if "TVsourcename" in item:
                via = "[%s via %s]" % (item["author"], item["TVsourcename"])
            else:
                via = "[%s]" % (item["author"])
        elif "TVsourceurl" in item:
            feedinfo, feedconfig = tv.aggregator.db.services.getserviceinfoandconfig(item["TVsourceurl"])
            via = '[<a href="%s">%s</a>]' % (feedconfig.get("publiclink",
                                                            item["TVsourceurl"]),
                                             feedconfig.get("publicname", ""))
            self.GetSource().SetLabel(feedconfig.get("publicname", ""))
        else:
            via = ""
        text = ("%s %s" % (item.get("description", "").strip(), via)).strip()
        self.GetPosttext().SetValue(text)

        # get categories if neened
        if catnames == None:
            dlg = wxProgressDialog("XML-RPC processing",
                                   "Geting categories from weblog",
                                   0,
                                   self,
                                   wxPD_APP_MODAL)
            try:
                
                catnames = tv.weblog.metaWeblog.getCategories().keys()
                catnames.sort()
            except:
                pass
                #raise
            dlg.Destroy()

        # add preview if possible
        if item.get("link", "").startswith("http://"):
            startAsyncFunc(self, urllib.urlopen, (item["link"]))
            if tv.config.get('ui.autopreview'):
                if wxPlatform == "__WXMSW__":
                    self.html = wxIEHtmlWin(self, -1, size=wxDLG_SZE(self, 300, 100), style = wxNO_FULL_REPAINT_ON_RESIZE|wxSUNKEN_BORDER)
                    self.html.Navigate(item["link"])
                    # Hook up the event handlers for the IE window
                    EVT_MSHTML_BEFORENAVIGATE2(self, -1, self.OnBeforeNavigate2)
                    EVT_MSHTML_NEWWINDOW2(self, -1, self.OnNewWindow2)
                    EVT_MSHTML_DOCUMENTCOMPLETE(self, -1, self.OnDocumentComplete)
                    EVT_MSHTML_TITLECHANGE(self, -1, self.OnTitleChange)
                else:
                    # Wxhtml seems to have problems if multiple windows are rendered. check this.
                    self.html = wxHtmlWindow(self, -1, size=wxDLG_SZE(self, 300, 100),
                                             style=wxSUNKEN_BORDER)
                self.html.SetPage("<html><body>loading page ...</body></center>")
                self.previewsizer.Add(self.html, 1, wxEXPAND)
                print self.html

        # add categories
        self.categories = []
        if catnames == None:
            self.catsizer.Add(wxStaticText(self, -1, "can't get categories"))
        else:
            for x in catnames:
                cID = NewId()
                cb = wxCheckBox(self, cID, x)
                self.categories.append(cb)
                self.catsizer.Add(cb)        

        # resizing to accomodate categories
        DialogElements.Fit(self)
        DialogElements.SetSizeHints(self) 

        # WDR: handler declarations for EditPost
        EVT_BUTTON(self, ID_SOURCE, self.OnSource)
        EVT_BUTTON(self, ID_CHANGEDATE, self.OnChangedate)
        EVT_BUTTON(self, ID_BROWSE, self.OnBrowse)
        EVT_BUTTON(self, ID_KILL, self.OnKill)
        EVT_BUTTON(self, wxID_POST, self.OnPost)
        EVT_SIZE(self, self.OnSize)
        EVT_ASYNCFUNC_DONE(self, self.OnAsyncFuncDone)
        

    # WDR: methods for EditPost

    def GetKill(self):
        return wxPyTypeCast( self.FindWindowById(ID_KILL), "wxButton" )

    def GetDate(self):
        return wxPyTypeCast( self.FindWindowById(ID_DATE), "wxStaticText" )

    def GetChangedate(self):
        return wxPyTypeCast( self.FindWindowById(ID_CHANGEDATE), "wxButton" )

    def GetSource(self):
        return self.FindWindowById(ID_SOURCE)
        #return wxPyTypeCast( self.FindWindowById(ID_SOURCE), "wxStaticText" )

    def GetBrowse(self):
        return wxPyTypeCast( self.FindWindowById(ID_BROWSE), "wxButton" )

    def GetPosttitle(self):
        return wxPyTypeCast( self.FindWindowById(ID_POSTTITLE), "wxTextCtrl" )

    def GetPostlink(self):
        return wxPyTypeCast( self.FindWindowById(ID_POSTLINK), "wxTextCtrl" )

    def GetPosttext(self):
        return wxPyTypeCast( self.FindWindowById(ID_POSTTEXT), "wxTextCtrl" )

    def GetPostingtext(self):
        return wxPyTypeCast( self.FindWindowById(ID_POSTINGTEXT), "wxStaticText" )

    def GetPostinggauge(self):
        return wxPyTypeCast( self.FindWindowById(ID_POSTINGGAUGE), "wxGauge" )

    # WDR: handler implementations for EditPost

    def OnSource(self, event):
        import TvService 
        dialog = TvService.ServiceDialog(self.parent, self.item.get("TVsourceurl"))
        dialog.Show()

    def OnChangedate(self, event):
        import wxPython.lib.calendar
        # year, month, day
        if self.targetdate is not None:
            dlg = wxPython.lib.calendar.CalenDlg(self,
                                                 month=self.targetdate.month,
                                                 day=self.targetdate.day,
                                                 year=self.targetdate.year)
        else:
            dlg = wxPython.lib.calendar.CalenDlg(self)
        dlg.Centre()
        if dlg.ShowModal() == wxID_OK:
            result = dlg.result
            self.targetdate = mx.DateTime.DateTimeFrom(int(result[3]),
                                                       int(dlg.calend.GetMonth()),
                                                       int(result[1]))
            self.GetDate().SetLabel(self.targetdate.strftime("%e. %B %Y (%D)"))
        else:
            print 'No Date Selected'
                                                                                                             
        pass

    def OnBrowse(self, event):
        import webbrowser
        webbrowser.open(self.GetPostlink().GetValue())

    def OnKill(self, event):
        self.Show(FALSE)
        self.Destroy()
        if self.killfunc:
            self.killfunc()

    def OnBeforeNavigate2(self, evt):
        self.logEvt('OnBeforeNavigate2', evt)

    def OnNewWindow2(self, evt):
        self.logEvt('OnNewWindow2', evt)
        evt.Veto() # don't allow it

    def OnDocumentComplete(self, evt):
        self.logEvt('OnDocumentComplete', evt)

    def OnTitleChange(self, evt):
        self.logEvt('OnTitleChange', evt)

    def OnStatusTextChange(self, evt):
        self.logEvt('OnStatusTextChange', evt)

    def logEvt(self, name, event):
        print ('%s: %s\n' %
                       (name, (event.GetLong1(), event.GetLong2(), event.GetText1())))

    def OnSize(self, event):
        self.Layout()

    def OnAsyncFuncDone(self, event):
        print "link arrived"
        url = event.GetReturnValue()
        link = url.geturl()
        if link != self.item.get("link", "").strip():
            if self.item.get("link", "").strip() == self.GetPostlink().GetValue():
                self.GetPostlink().SetValue(link)
        if tv.config.get('ui.autopreview'):
            if wxPlatform == "__WXMSW__":
                pass
            else:
                self.html.SetPage(url.read())
        
        
    def OnPost(self, event):
        print "posting"
        
        # XXX: fixme - Build a Posting from the Dialog Data
        # fixme - show gauge
        info = self.GetPostingtext()
        info.SetLabel("Generating entry")
        info.GetContainingSizer().SetItemMinSize(info,
                                                 info.GetSize().GetWidth(),
                                                 info.GetSize().GetHeight())
        info.GetContainingSizer().Layout()

        self.post = {}
        x = self.GetPosttext().GetValue()
        if x:
            self.post['description'] = tv.weblog.tools.escape(x)
        x = self.GetPosttitle().GetValue()
        if x:
            self.post['title'] = tv.weblog.tools.escape(x)
        x = self.GetPostlink().GetValue()
        if x:
            if x != self.item.get('link') and self.item.get('link') is not None:
                source = self.item['link']
            self.post['link'] = x
        self.post['categories'] = []
        for x in self.categories:
            if x.GetValue():
                self.post['categories'].append(x.GetLabel())
        info.SetLabel("Sending to Weblog")
        print "Sending to Weblog"
        try:
            wxYield()
            postid = tv.weblog.metaWeblog.newPost(self.post)            
            wxYield()
            print postid
            print "posted"
            if self.targetdate is not None:
                info.SetLabel("setting date")
                wxYield()
                tv.weblog.metaWeblog.newDateForPost(postid, (self.targetdate.year,
                                                             self.targetdate.month,
                                                             self.targetdate.day,
                                                             self.targetdate.hour,
                                                             self.targetdate.minute,
                                                             self.targetdate.second))
                wxYield()
                
            # XXX: set source
            info.SetLabel("Done")

            self.Show(FALSE)
            self.Destroy()
            
            # delete posting
            # XXX: Test if user want'S killing after posting.
            if self.killfunc:
                self.killfunc()
        except RuntimeError, msg: 
            info.SetLabel("Error: %r" % msg)
