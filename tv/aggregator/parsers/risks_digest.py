import StringIO
import urllib
import rfc822

risksurl = "http://www.csl.sri.com/users/risko/risks.txt"
itemsplitter = "\n------------------------------\n\n"
linkbase = "http://catless.ncl.ac.uk/go/risks/"

"""
title
link
description

Optional channel elements 
language
copyright
managingEditor
webMasterEmail
pubDate
lastBuildDate
category
generator
docs
cloud
ttl
image




"""
title
link
description
author
category
comments
enclosure
guid <guid isPermaLink="true">http://inessential.com/2002/09/01.php#a2</guid>
pubDate
source
"""

from pprint import pprint

fp = urllib.urlopen(risksurl)
page = fp.read()
items = page.split(itemsplitter)
header = rfc822.Message(StringIO.StringIO(items[0]))
footer = rfc822.Message(StringIO.StringIO(items[-1]))
items = items[1:-2]
itemnr = 1
volumeissue = header.get('subject')
volume, issue = volumeissue[volumeissue.rindex(" ")+1:].split(".")
volumeissuepath =  "%s%2d/%2d" % (linkbase, int(volume), int(issue))
for x in items:
    item = {}
    fobj = StringIO.StringIO(x)
    m = rfc822.Message(fobj)
    item["link"] =  "%s/%d" % (volumeissuepath, itemnr)
    item["pubDate"] = m.get('date')
    item["autor"] = m.get('from')
    item["title"] = m.get('subject')
    item["description"] = "<pre>\n%s</pre>" % m.fp.read()
    pprint(item)  
    itemnr += 1
