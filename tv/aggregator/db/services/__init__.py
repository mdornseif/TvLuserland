""" DB functions for services (RSS feeds)

Services are saved in a bsddb as a dictionary of dictionarys. the
first level of dicionary contains items related to different parts of
the aggregator. At the moment there are only two entries defined:
'feedinfo' and 'feedconfig'. feedinfo is only to be written by the thread
reading rss files from the network, 'feedconfig' is only to be written by the GUI. 

"""

__rcsid__ = "$Id: __init__.py,v 1.8 2002/12/23 18:58:58 drt Exp $"

# Try using cPickle and cStringIO if available.
try:
    from cPickle import load, dump, loads, dumps
except ImportError:
    from pickle import load, dump, loads, dumps
    
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

                                
import os, os.path
import atexit
import threading
import cgi
import time
from bsddb3 import db
import mx.DateTime

import tv.config
from tv.aggregator.db import _dbenv

from tv.thirdparty import opml_parser

_picklecache = {}

def pickle(object):
    global _picklecache

    # trim cache:this is extremly crude
    if len(_picklecache) > 1000:
        _picklecache = {}
    x = dumps(object, 1)
    _picklecache[x] = object
    return x
    
def unpickle(string):
    global _picklecache
    try:
        return _picklecache[string]
    except KeyError:
        x = _picklecache[string] = loads(string)
        return x

def init():
    global _servicedb

    # create and open the DB
    _servicedb = db.DB(_dbenv)
    _servicedb.open("services",   
                    dbtype = db.DB_BTREE,
                    flags = db.DB_CREATE|db.DB_THREAD,
                    mode = 0644)
    atexit.register(close)


def close():
    savesubscriptions(getsubscriptions())
    _servicedb.close()

def getservices():
    return _servicedb.keys()

def getservice(sourceurl):
    d = _servicedb.get(sourceurl)
    if d:
        data = unpickle(d)
        if data.keys() == ["feedinfo", "config"] or data.keys() == ["config", "feedinfo"]:
            # convert old data from db
            data = {"feedinfo": data["feedinfo"],
                    "feedconfig": data["config"]}
        # check and fix some errors
        if "publicname" not in data["feedconfig"]:
            data["feedconfig"]["publicname"] = data["feedinfo"].get("title", "-none-")
        if "privatename" not in data["feedconfig"]:
            data["feedconfig"]["privatename"] = data["feedconfig"].get("publicname", "-none-")
        if data["feedconfig"].get("publiclink", "") == "":
            data["feedconfig"]["publiclink"] = data["feedinfo"].get("link", "-none-" )
    else:
        # new entry
        data = {"feedinfo": {"TVsourceurl": sourceurl, "TVcreated": mx.DateTime.now()},
                "feedconfig": {}}
    return data

def getserviceinfoandconfig(sourceurl):
    x = getservice(sourceurl)
    return (x["feedinfo"], x["feedconfig"])

def getserviceflat(sourceurl):
    data = getservice(sourceurl)
    ret = data["feedinfo"]
    ret.update(data["feedconfig"])
    return ret

def getfeedinfo(sourceurl):
    return getservice(sourceurl)["feedinfo"]


def getfeedconfig(sourceurl):
    return getservice(sourceurl)["feedconfig"]

def saveservice(service):
    d = pickle(service)
    _servicedb.put(key=service["feedinfo"]["TVsourceurl"], data=d), # , flags=db.DB_NOOVERWRITE)    

writelock = threading.Lock()

def savefeedinfo(feedinfo):
    writelock.acquire()
    saveservice({"feedinfo": feedinfo, "feedconfig": getfeedconfig(feedinfo["TVsourceurl"])})
    writelock.release()
    

def savefeedconfig(sourceurl, feedconfig):
    writelock.acquire()
    saveservice({"feedinfo": getfeedinfo(sourceurl), "feedconfig": feedconfig})
    writelock.release()

feedinfo_cachetime = 0
feedinfo_cache = None

# XXX: We should generate a cache here to get rid of the fastsave hack
def getsubscriptions():
    ret = []
    try:
        if os.stat(os.path.join(tv.config.get("fs.dbdir"), "subscriptions.opml")).st_mtime < feedinfo_cachetime:
            ret = feedinfio_cache
        else:
            for x in opml_parser.load(os.path.join(tv.config.get("fs.dbdir"), "subscriptions.opml")):
                ret.append(x[1])
            feedinfo_cache = ret
            feedinfo_cacchetime = time.time()
    except IOError:
        ret = ["http://radio.weblogs.com/0112292/rss.xml"]
    except OSError:
        ret = ["http://radio.weblogs.com/0112292/rss.xml"]
    return ret

def savesubscriptions(subscriptions):
    print "generating", time.time()
    feedinfo_cache = subscriptions
    feedinfo_cacchetime = time.time()
    outlines = []
    for x in subscriptions:
        feedinfo, feedconfig = getserviceinfoandconfig(x)
        title = feedconfig.get("publicname", feedinfo.get("title", "Unknown title for: %s" % x))
        outlines.append('<outline title="%s" xmlUrl="%s" />' % (title.replace("&", "&amp;"), x.replace("&", "&amp;")))

    print "saving", time.time()
    fd = open(os.path.join(tv.config.get("fs.dbdir"), "subscriptions.opml"), 'w')
    fd.write('''<opml version="1.0">
<body>
%s
</body>
</opml>
''' % "\n".join(outlines))
    fd.close()
    print "done", time.time()

def fastsavesubscriptions(subscriptions):
    print "generating", time.time()
    feedinfo_cache = subscriptions
    feedinfo_cacchetime = time.time()
    outlines = []
    for x in subscriptions:
          outlines.append('<outline xmlUrl="%s" />' % (x.replace("&", "&amp;")))

    print "saving", time.time()
    fd = open(os.path.join(tv.config.get("fs.dbdir"), "subscriptions.opml"), 'w')
    fd.write('''<opml version="1.0">
<body>
%s
</body>
</opml>
''' % "\n".join(outlines))
    fd.close()
    print "done", time.time()

def issubscribed(serviceurl):
    return serviceurl in getsubscriptions()
                               

def subscribe(serviceurl):
    subscriptions = getsubscriptions()
    if serviceurl not in subscriptions:
        subscriptions.append(serviceurl)
        fastsavesubscriptions(subscriptions)
        return 1
    return None

def unsubscribe(serviceurl):
    subscriptions = getsubscriptions()
    if serviceurl not in subscriptions:
        return None
    else:
        newsub = []
        for x in subscriptions:
            if x != serviceurl:
                newsub.append(x)
        fastsavesubscriptions(newsub)

init()
