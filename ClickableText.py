
__rcsid__ = "$Id: ClickableText.py,v 1.3 2002/11/05 10:49:02 drt Exp $"

from wxPython.wx import *
from wxPython.lib.buttons import  wxGenButtonEvent

import webbrowser

class wxClickableText(wxPyControl):
    """ wxClickableText - A Text Control wich handles resizing itself
    after the Label changes, generates clicks for events and is able to
    change font and colour.
    
    based on: Robin Dunn's wxGenStaticText and lib.buttons
    """
    
    def __init__(self, parent, ID, label,
                 pos = wxDefaultPosition, size = wxDefaultSize,
                 style = 0, validator = wxDefaultValidator,
                 name = "clickabletext"):
        if style == 0:
            style = wxNO_BORDER
        wxPyControl.__init__(self, parent, ID, pos, size, style, validator, name)

        self.downColour = wxRED
        self.up = true

        wxPyControl.SetLabel(self, label) # don't check wxST_NO_AUTORESIZE yet
        self.SetPosition(pos)
        font = parent.GetFont()
        if not font.Ok():
            font = wxSystemSettings_GetSystemFont(wxSYS_DEFAULT_GUI_FONT)
        wxPyControl.SetFont(self, font)  # same here
        self.SetBestSize(size)

        EVT_LEFT_DOWN(self,        self.OnLeftDown)
        EVT_LEFT_UP(self,          self.OnLeftUp)
        if wxPlatform == '__WXMSW__':
            EVT_LEFT_DCLICK(self,  self.OnLeftDown)
        EVT_MOTION(self,           self.OnMotion)
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        EVT_PAINT(self,            self.OnPaint)

    def SetLabel(self, label):
        """
        Sets the static text label and updates the control's size to exactly
        fit the label unless the control has wxST_NO_AUTORESIZE flag.
        """
        wxPyControl.SetLabel(self, label)
        style = self.GetWindowStyleFlag()
        if not style & wxST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
            self.GetContainingSizer().SetItemMinSize(self,
                                                     self.GetSize().GetWidth(),
                                                     self.GetSize().GetHeight())

            self.GetContainingSizer().Layout()

    def SetFont(self, font):
        """
        Sets the static text font and updates the control's size to exactly
        fit the label unless the control has wxST_NO_AUTORESIZE flag.
        """
        wxPyControl.SetFont(self, font)
        style = self.GetWindowStyleFlag()
        if not style & wxST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())


    def SetBestSize(self, size=None):
        """
        Given the current font and bezel width settings, calculate
        and set a good size.
        """
        if size is None:
            size = wxSize(-1,-1)
        if type(size) == type(()):
            size = wxSize(size[0], size[1])
        size = wxSize(size.width, size.height)  # make a copy

        best = self.GetBestSize()
        if size.width == -1:
            size.width = best.width
        if size.height == -1:
            size.height = best.height

        self.SetSize(size)


    def DoGetBestSize(self):
        """Overridden base class virtual.  Determines the best size of the
        button based on the label and bezel size."""
        w, h, useMin = self._GetLabelSize()
        return (w, h)


    def AcceptsFocus(self):
        """Overridden base class virtual."""
        return FALSE


    def _GetLabelSize(self):
        """ used internally """
        w, h = self.GetTextExtent(self.GetLabel())
        return w, h, true


    def Notify(self):
        evt = wxGenButtonEvent(wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        evt.SetIsDown(true)
        evt.SetButtonObj(self)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)



    def DrawLabel(self, dc, width, height, dw=0, dy=0):
        dc.SetFont(self.GetFont())
        if self.IsEnabled():
            if self.up:
                dc.SetTextForeground(self.GetForegroundColour())
            else:
                dc.SetTextForeground(self.downColour)                
        else:
            dc.SetTextForeground(wxSystemSettings_GetSystemColour(wxSYS_COLOUR_GRAYTEXT))
        label = self.GetLabel()
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (width-tw)/2+dw, (height-th)/2+dy)



    def OnPaint(self, event):
        (width, height) = self.GetClientSizeTuple()
        x1 = y1 = 0
        x2 = width-1
        y2 = height-1
        dc = wxBufferedPaintDC(self)
        dc.SetBackgroundMode(wxTRANSPARENT)
        dc.Clear()
        self.DrawLabel(dc, width, height)

    def OnEraseBackground(self, event):
        pass


    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        self.up = false
        #self.CaptureMouse()
        #self.SetFocus()
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        if not self.IsEnabled():
            return
        #self.ReleaseMouse()
        self.up = true
        self.Refresh()
        self.Notify()
        event.Skip()


    def OnMotion(self, event):
        if not self.IsEnabled():
            return
        if event.LeftIsDown():
            x,y = event.GetPositionTuple()
            w,h = self.GetClientSizeTuple()
            if self.up and x<w and x>=0 and y<h and y>=0:
                self.up = false
                self.Refresh()
                return
            if not self.up and (x<0 or y<0 or x>=w or y>=h):
                self.up = true
                self.Refresh()
                return
        event.Skip()




class wxLinkText(wxClickableText):
    """Display a URL similar to static text but open it in a WEbbrowser if a user clicks on it."""

    def __init__(self, parent, ID, label,
                 pos = wxDefaultPosition, size = wxDefaultSize,
                 style = 0, validator = wxDefaultValidator,
                 name = "linktext"):
        wxClickableText.__init__(self, parent, ID, label, pos, size, style, validator, name)
        self.SetForegroundColour(wxBLUE)


    def OnLeftUp(self, event):
        wxClickableText.OnLeftUp(self, event)
        if self.IsEnabled():
            webbrowser.open(self.GetLabel())
        event.Skip()
