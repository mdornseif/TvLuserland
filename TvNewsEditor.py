from wxPython.wx import *
from wxPython.html import *

from TvLuserland_wdr import *

import tv.weblog.metaWeblog
import tv.aggregator.db.services
import tv.config

# category cache
catnames = None

# constants

ID_QUIT = 100

# WDR: classes
  
class EditPostDialog(wxDialog):
    def __init__(self, parent, id, title = None,
        pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        style = wxDEFAULT_DIALOG_STYLE, item = {}, killfunc = None ):
        global catnames

        self.item = item
        self.killfunc = killfunc
        if title == None:
            title = "Posting: %s" % (item.get("title", ""))

        wxDialog.__init__(self, parent, id, title, pos, size, style)
        
        DialogElements = EditPostFunc( self, true )

        # preset content if wanted
        self.GetPosttitle().SetValue(item.get("title", "").strip())
        self.GetPostlink().SetValue(item.get("link", "").strip())
        if "TVsourceurl" in item:
            service = tv.aggregator.db.services.getservice(item["TVsourceurl"])
            via = '[<a href="%s">%s</a>]' % (service.get("link",
                                                         item["TVsourceurl"]),
                                             service.get("title",
                                                         service.get("managingEditor",
                                                                     service.get("webMaster", "source"))))
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

        # add preview if possible and wanted
        if "link" in item and tv.config.get("ui.autopreview"):
            self.html = wxHtmlWindow(self, -1, size=wxDLG_SZE(self, 300, 100),
                                     style=wxSIMPLE_BORDER)
            self.html.SetPage("<html><body>loading page ...</body></center>")
            self.html.LoadPage(item["link"])
            self.previewsizer.Add(self.html)


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
        EVT_BUTTON(self, wxID_POST, self.OnPost)

    # WDR: methods for EditPost

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

    def OnPost(self, event):
        print "posting"
        # Build a Posting from the Dialog Data
        self.GetPostingtext().SetLabel("Generating entry")
        self.item = {}
        x = self.GetPosttext().GetValue()
        if x:
            self.item['description'] = x
        x = self.GetPosttitle().GetValue()
        if x:
            self.item['title'] = x
        x = self.GetPostlink().GetValue()
        if x:
            self.item['link'] = x
        self.item['categories'] = []
        for x in self.categories:
            if x.GetValue():
                self.item['categories'].append(x.GetLabel())
        self.GetPostingtext().SetLabel("Sending to Weblog")
        # XXX: The Label has to reposition itself
        tv.weblog.metaWeblog.newPost(self.item)            
        self.GetPostingtext().SetLabel("Done")
        self.Show(FALSE)
        # XXX: delete posting
        if self.killfunc:
            self.killfunc()
        
