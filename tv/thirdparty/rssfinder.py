"""Ultra-liberal RSS feed locator

Usage:
getFeeds(uri) - returns list of RSS feeds associated with this address

Example:
>>> import rssfinder
>>> rssfinder.getFeeds('http://diveintomark.org/')
['http://diveintomark.org/xml/rss.xml']
>>> rssfinder.getFeeds('macnn.com')
['http://www.macnn.com/macnn.rdf']

Can also use from the command line.  Feeds are returned one per line:
$ python rssfinder.py diveintomark.org
http://diveintomark.org/xml/rss.xml

How it works:
0. At every step, RSS feeds are minimally verified to make sure they are
   really RSS feeds.
1. If the URI points to an RSS feed, it is simply returned; otherwise
   the page is downloaded and the real fun begins.
2. Feeds pointed to by LINK tags in the header of the page (RSS autodiscovery)
3. <A> links to feeds on the same server ending in ".rss", ".rdf", or ".xml"
4. <A> links to feeds on the same server containing "rss", "rdf", or "xml"
5. <A> links to feeds on external servers ending in ".rss", ".rdf", or ".xml"
6. <A> links to feeds on external servers containing "rss", "rdf", or "xml"
7. As a last ditch effort, we search Syndic8 for feeds matching the URI
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__copyright__ = "Copyright 2002, Mark Pilgrim"
__license__ = "GPL"
__credits__ = """Abe Fettig for a patch to sort Syndic8 feeds by popularity
Also Jason Diamond, Brian Lalor for bug reporting and patches"""

_debug = 0
try:
    import xmlrpclib # http://www.pythonware.com/products/xmlrpc/
except ImportError:
    pass
from sgmllib import SGMLParser
import urllib, urlparse, re, sys

class BaseParser(SGMLParser):
    def __init__(self, baseuri):
        SGMLParser.__init__(self)
        self.links = []
        self.baseuri = baseuri
        
class LinkParser(BaseParser):
    RSSTYPE = ('application/rss+xml', 'text/xml')
    def do_link(self, attrs):
        rels = [v for k,v in attrs if k=='rel']
        if not rels: return
        if rels[0].lower() <> 'alternate': return
        types = [v for k,v in attrs if k=='type']
        if not types: return
        type = types[0]
        isRSSType = 0
        for t in self.RSSTYPE:
            isRSSType = type.startswith(t)
            if isRSSType: break
        if not isRSSType: return
        hrefs = [v for k,v in attrs if k=='href']
        if not hrefs: return
        self.links.append(urlparse.urljoin(self.baseuri, hrefs[0]))

class ALinkParser(BaseParser):
    def start_a(self, attrs):
        hrefs = [v for k,v in attrs if k=='href']
        if not hrefs: return
        self.links.append(urlparse.urljoin(self.baseuri, hrefs[0]))

def makeFullURI(uri):
    if not uri.count('http://'):
        uri = 'http://%s' % uri
    return uri

def getLinks(data, baseuri):
    p = LinkParser(baseuri)
    p.feed(data)
    return p.links

def getALinks(data, baseuri):
    p = ALinkParser(baseuri)
    p.feed(data)
    return p.links

def getLocalLinks(links, baseuri):
    baseuri = baseuri.lower()
    urilen = len(baseuri)
    return [l for l in links if l.lower().startswith(baseuri)]

def isFeedLink(link):
    return link[-4:].lower() in ('.rss', '.rdf', '.xml')

def isXMLRelatedLink(link):
    link = link.lower()
    return link.count('rss') + link.count('rdf') + link.count('xml')

def isRSS(data):
    data = data.lower()
    if data.count('<html'): return 0
    return data.count('<rss') + data.count('<rdf')

def isFeed(uri):
    if _debug: print 'verifying that %s is a feed' % uri
    try:
        protocol = urlparse.urlparse(uri)
        if protocol[0] in ('http', 'https'):
            usock = urllib.urlopen(uri)
            data = usock.read()
            usock.close()
            if isRSS(data):
                return data
            return 0
        else:
            return 0
    except:
        return 0

def sortFeeds(feed1Info, feed2Info):
    return cmp(feed2Info['headlines_rank'], feed1Info['headlines_rank'])

def getFeedsFromSyndic8(uri):
    feeds = []
    try:
        server = xmlrpclib.Server('http://www.syndic8.com/xmlrpc.php')
        feedids = server.syndic8.FindFeeds(uri)
        infolist = server.syndic8.GetFeedInfo(feedids, ['headlines_rank','status','dataurl'])
        infolist.sort(sortFeeds)
        feeds = [f['dataurl'] for f in infolist if f['status']=='Syndicated']
        if _debug: print 'found %s feeds through Syndic8' % len(feeds)
    except:
        pass
    return feeds

def getRealFeeds(uris):
    feeds = []
    for u in uris:
        res = isFeed(u)
        if res:
            feeds.append((u, res))
    return feeds
    
def getFeeds(uri):
    fulluri = makeFullURI(uri)
    usock = urllib.urlopen(fulluri)
    data = usock.read()
    usock.close()
    # is this already a feed?
    if isRSS(data):
        return [fulluri]
    # nope, it's a page, try LINK tags first
    if _debug: print 'looking for LINK tags'
    feeds = getLinks(data, fulluri)
    if _debug: print 'found %s feeds through LINK tags' % len(feeds)
    #    feeds = filter(isFeed, feeds)
    feeds = getRealFeeds(feeds)
    if not feeds:
        # no LINK tags, look for regular <A> links that point to feeds
        if _debug: print 'no LINK tags, looking at A tags'
        links = getALinks(data, fulluri)
        locallinks = getLocalLinks(links, fulluri)
        # look for obvious feed links on the same server
        #feeds = filter(isFeed, filter(isFeedLink, locallinks))
        feeds = getRealFeeds(filter(isFeedLink, locallinks))
        if not feeds:
            # look harder for feed links on the same server
            #feeds = filter(isFeed, filter(isXMLRelatedLink, locallinks))
            feeds = getRealFeeds(filter(isXMLRelatedLink, locallinks))
        if not feeds:
            # look for obvious feed links on another server
            #feeds = filter(isFeed, filter(isFeedLink, links))
            feeds = getRealFeeds(filter(isFeedLink, links))
        if not feeds:
            # look harder for feed links on another server
            #feeds = filter(isFeed, filter(isXMLRelatedLink, links))
            feeds = getRealFeeds(filter(isXMLRelatedLink, links))
    if not feeds:
        # still no luck, search Syndic8 for feeds (requires xmlrpclib)
        if _debug: print 'still no luck, searching Syndic8'
        feeds = getRealFeeds(getFeedsFromSyndic8(uri))
    return feeds

if __name__ == '__main__':
    if sys.argv[1:]:
        uri = sys.argv[1]
    else:
        uri = 'http://diveintomark.org/'
    print "\n".join(getFeeds(uri))
