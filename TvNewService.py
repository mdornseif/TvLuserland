#!/bin/env python
#----------------------------------------------------------------------------
# Name:         TvServiceList.py
# Author:       XXXX
# Created:      XX/XX/XX
# Copyright:    
#----------------------------------------------------------------------------

import types

from wxPython.wx import *

import tv.aggregator.db.services
from TvLuserland_wdr import *

from tv.thirdparty.rssfinder import getFeeds
import tv.aggregator.db.services

def NewService(parent):
    dlg = wxTextEntryDialog(parent,
                            'Which Service to add ? Enter the URL of the RSS feed or th webpage you want to subscribe to.',
                            'New Service', )
    dlg.SetValue("http://")
    dlg.CentreOnParent()
    if dlg.ShowModal() == wxID_OK:
        url = dlg.GetValue()
        dlg.Destroy()

        dlg = wxProgressDialog("Processing new Services",
                               "Finding and verifying feeds for the URL you gave me. This might take some time.",
                               0,
                               parent,
                               wxPD_APP_MODAL)
        dlg.CentreOnParent()
        #keepGoing = dlg.Update(count, "Half-time!")

        feeds = getFeeds(url)
        print "feeds arrived"

        problem = None
        newfeeds = []
        oldfeeds = []
        for x in feeds:
            if type(x) == types.TupleType:
                x = x[0]
            if not tv.aggregator.db.services.issubscribed(x):        
                newfeeds.append(x)
            else:
                oldfeeds.append(x)

        
        if len(feeds) == 0:
            problem = "I was not able to find any XML/RSS feeds at %r." % (url) 
        elif len(newfeeds) == 0:
            problem = "I was not able to find new XML/RSS feeds at %r.There where %d feeds, but you are already subscribed to all of them. (%r)" % (url, len(oldfeeds), oldfeeds)
    
        feeds = newfeeds        
        dlg.Destroy()

        if problem:
            dlg = wxMessageDialog(parent, problem,
                                  'Problem subscribing',
                                  wxOK | wxICON_HAND)
            dlg.ShowModal()
            dlg.Destroy()
            return


        if len(feeds) > 1:
            dlg = wxSingleChoiceDialog(parent, 'I found more than on feed referenced by your input. Please Choose one.',
                                       'Select Feed',
                                       feeds, wxOK|wxCANCEL)
            
            dlg.CentreOnParent()
            if dlg.ShowModal() == wxID_OK:
                serviceurl = dlg.GetStringSelection()
                dlg.Destroy()
            else:
                return
                
        else:
            serviceurl = feeds[0]

        tv.aggregator.db.services.subscribe(serviceurl)
        
        # XXX
        dlg = wxMessageDialog(parent, "You are subscribed now to %r. If I was an finished application I would now fetch data from the newly subscribed Service and present you some Service configuration Options. I'm not so you hafe to wait until the next fetching cycle is done. (Hint: Start rssfetch.py)" % sourceurl,
                                  'Done',
                                  wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
        print serviceurl, url, feeds

        
                            
