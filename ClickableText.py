# based on:

#----------------------------------------------------------------------
# Name:        wxPython.lib.stattext
# Purpose:     A generic wxGenStaticText class.  Using this should
#              eliminate some of the platform differences in wxStaticText,
#              such as background colours and mouse sensitivity.
#
# Author:      Robin Dunn
#
# Created:     8-July-2002
# RCS-ID:      $Id: ClickableText.py,v 1.1 2002/10/31 22:35:09 drt Exp $
# Copyright:   (c) 2002 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

"""
"""

from wxPython.wx import *
import string

#----------------------------------------------------------------------

class wxClickableText(wxPyControl):
    labelDelta = 1

    def __init__(self, parent, ID, label,
                 pos = wxDefaultPosition, size = wxDefaultSize,
                 style = 0,
                 name = "genstattext"):
        wxPyControl.__init__(self, parent, ID, pos, size, style, wxDefaultValidator, name)

        wxPyControl.SetLabel(self, label) # don't check wxST_NO_AUTORESIZE yet
        self.SetPosition(pos)
        font = parent.GetFont()
        if not font.Ok():
            font = wxSystemSettings_GetSystemFont(wxSYS_DEFAULT_GUI_FONT)
        wxPyControl.SetFont(self, font) # same here

        clr = parent.GetBackgroundColour()
        if not clr.Ok():
            clr = wxSystemSettings_GetSystemColour(wxSYS_COLOUR_BTNFACE)
        self.SetBackgroundColour(clr)

        clr = parent.GetForegroundColour()
        if not clr.Ok():
            clr = wxSystemSettings_GetSystemColour(wxSYS_COLOUR_BTNTEXT)
        self.SetForegroundColour(clr)

        rw, rh = size
        bw, bh = self.GetBestSize()
        if rw == -1: rw = bw
        if rh == -1: rh = bh
        self.SetSize(wxSize(rw, rh))

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


    def DoGetBestSize(self):
        """Overridden base class virtual.  Determines the best size of the
        button based on the label size."""
        label = self.GetLabel()
        maxWidth = totalHeight = 0
        for line in label.split('\n'):
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)
            totalHeight += h
            maxWidth = max(maxWidth, w)
        return wxSize(maxWidth, totalHeight)


    def AcceptsFocus(self):
        """Overridden base class virtual."""
        return false


    def OnPaint(self, event):
        width, height = self.GetClientSize()
        dc = wxBufferedPaintDC(self)
        dc.SetBackground(wxBrush(self.GetBackgroundColour(), wxSOLID))
        dc.Clear()
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        style = self.GetWindowStyleFlag()
        x = y = 0
        for line in label.split('\n'):
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)
            if style & wxALIGN_RIGHT:
                x = width - w
            if style & wxALIGN_CENTER:
                x = (width - w)/2
            dc.DrawText(line, x, y)
            y += h


    def OnEraseBackground(self, event):
        pass




#----------------------------------------------------------------------


