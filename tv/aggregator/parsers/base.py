
import mx.DateTime
import mx.DateTime.Parser

class ParserPluginBase:
    __description__ = "Description of the parser"
    __suggestedSourceUrls__ = [("http://ecample.com/", "Example Feed")]

    
    def __init__(self, url):
        self.url = url
        self.itemlist = []

    def process(self):
        self.fetch(self.url)
        self.parse()
        

    def fetch(self, url, etag=None, modified=None):
        """Does a conditional http get, returns a tuple (data, etag, modified).

        If conditional get results in no new data it retuns (None, etag, Last-Modified).
        """
        import urllib

        # minimal, dump implementation
        self.url = url
        self.rawdata = urllib.urlopen(url).read()
        self.etag = None
        self.modified = mx.DateTime.now()
        return (self.rawdata, self.etag, self.modified)


    def parse(self, data, modified):
        pass

    def getChannel(self):
        """Returns a dict with something like a RSS channel
        description. In fact a dict doesn't allow us to express
        attributes, might be fixed some day"""

        # Some mock-ups for cut and pasting in child classes
        channel = {}
        channel["title"] = ""
        channel["link"] = ""
        channel["description"] = ""
        
        # Optional channel elements 
        channel["language"] = ""
        channel["copyright"] = ""
        channel["managingEditor"] = ""
        channel["webMasterEmail"] = ""
        channel["pubDate"] = ""
        channel["lastBuildDate"] = ""
        channel["category"] = ""
        channel["generator"] = ""
        channel["docs"] = ""
        channel["cloud"] = ""
        channel["ttl"] = ""
        channel["image"] = ""
       

    def getItems(self):
        """Returns a list of dictionarys with newsitems
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
        return self.itemlist

class SplittingParser(ParserPluginBase):
    def __init__(self, url):
        self.itemsplitter = "undef"
        self.linkbase = "undef"
        self.url = url
        ParserPluginBase.__init__(self)

    def fixDataForSplitting(self):
        pass

    def splitItems(self):
        return self.rawdata.split(self.itemsplitter)

    def fixItems(self, items):
        return items

    def processItem(self, rawitem):
        raise NotImplementedError

    def parse(self):
        self.fixDataForSplitting()
        items = self.splitItems()
        items = self.fixItems(items)
        for x in items:
            self.itemlist.append(self.processItem(x))


import StringIO
import rfc822

class RisksParser(SplittingParser):
    __description__ = "Parses the risks-digest"
    __suggestedSourceUrls__ = [("http://www.csl.sri.com/users/risko/risks.txt", "risks-digest web archive")]

    def __init__(self, url ="http://www.csl.sri.com/users/risko/risks.txt"):
        ParserPluginBase.__init__(self, url)
        self.itemsplitter = "\n------------------------------\n\n"
        # Seen in risks 16.15:
        #self.itemsplitter = "\n----------------------------\n\n"
        self.linkbase = "http://catless.ncl.ac.uk/go/risks/"
        # for counting items
        self.itemnr = 1
        
    def getChannel(self):
        """Returns a dict with something like a RSS channel
        description. In fact a dict doesn't allow us to express
        attributes, might be fixed some day"""

        # Some mock-ups for cut and pasting in child classes
        channel = {}
        channel["title"] = "risks-digest"
        channel["link"] = "http://catless.ncl.ac.uk/Risks"
        channel["description"] = "Forum On Risks To The Public In Computers And Related Systems - ACM Committee on Computers and Public Policy, Peter G. Neumann, moderator"
        
        # Optional channel elements 
        channel["language"] = "en"
        channel["managingEditor"] = "risks@csl.sri.com"
        channel["webMasterEmail"] = "lindsay.marshall@ncl.ac.uk"
        channel["pubDate"] = str(self.modified)
        channel["TVmodified"] = self.modified
        channel["TVlastfetched"] = mx.DateTime.now()
        return channel

    def fixItems(self, items):
        self.header = rfc822.Message(StringIO.StringIO(items[0]))
        self.footer = rfc822.Message(StringIO.StringIO(items[-1]))
        volumeissue = self.header.get('subject')
        self.volume, self.issue = volumeissue[volumeissue.rindex(" ")+1:].split(".")
        self.volumeissuepath =  "%s%02d/%02d/" % (self.linkbase, int(self.volume), int(self.issue))
        firstitem = items[0].split("\n------------------------------")[-1]
        firstitem = firstitem[firstitem.find("\n"):]
        return [firstitem] + items[1:-2]


    def processItem(self, rawitem):
        item = {}
        fobj = StringIO.StringIO(rawitem.strip())
        m = rfc822.Message(fobj)
        item["guid"] =  "%s%d" % (self.volumeissuepath, self.itemnr)
        if int(self.volume) > 20:
            item["link"] = item["guid"]
            item["source"] = self.volumeissuepath
        else:
            item["link"] = self.url
        item["pubDate"] = m.get('date')
        item["author"] = m.get('from')
        item["title"] = m.get('subject')
        item["description"] = ("%s" % m.fp.read()).replace("\n\n","\n<p>\n\n")
        item["TVsourcename"] = "risks-digest Volume %s, Issue %s" % (self.volume, self.issue)
        item["TVsourceurl"] = self.url
        try:
            item["TVdateobject"] = mx.DateTime.Parser.DateTimeFromString(m.get("date"))
        except: # ValueError or mx.DateTime.RangeErrorx
            item["TVdateobject"] = None
            d = m.get("date")
            while item["TVdateobject"] == None:
                print d
                d = d[:d.rfind(" ")]
                if len(d) < 10:
                    item["TVdateobject"] = mx.DateTime.now()
                    break
                try:
                    item["TVdateobject"] = mx.DateTime.Parser.DateTimeFromString(m.get("date")[:m.get("date").rfind(" ")])
                except: # ValueError or mx.DateTime.RangeError
                    pass
        self.itemnr += 1
        return item


import mx.DateTime, mx.DateTime.Parser
import tv.aggregator.db.items
import tv.aggregator.db.services
from pprint import pprint


def processPlugin():
    r = RisksParser()
    service, feedconfig = tv.aggregator.db.services.getserviceinfoandconfig(r.url)
    #pprint((service, feedconfig))
    if mx.DateTime.now() < service.get("TVlastfetched", mx.DateTime.DateTime(0)) + mx.DateTime.TimeDelta(minutes=feedconfig.get("fetchhowoften", 60)):
        print "will wait until at least %s for next fetch (%d minutes after last fetch)" % (service.get("TVlastfetched") + mx.DateTime.TimeDelta(minutes=feedconfig.get("fetchhowoften", 60)), feedconfig.get("fetchhowoften", 60))
        return
    r.process()
    service.update(r.getChannel())
    for x in r.getItems():
        print x["title"], x["guid"],
        if tv.aggregator.db.items.checkdupe(x):
            print "-",
        else:
            service["TVitemsfetched"] = service.get("TVitemsfetched", 0) + 1
            service["TVlastnewitem"] = mx.DateTime.now() 
            tv.aggregator.db.items.saveitem(x)
            print "*",
        print

processPlugin()


