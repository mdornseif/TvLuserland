""" DB functions for services (RSS feeds)

Services are saved in a bsddb as a dictionary of dictionarys. the
first level of dicionary contains items related to different parts of
the aggregator. At the moment there are only two entries defined:
'feedinfo' and 'config'. feedinfo is only to be written by the thread
reading rss files from the network, 'config' is only to be written by the GUI. 

"""

__rcsid__ = "$Id: __init__.py,v 1.5 2002/11/04 22:43:55 drt Exp $"

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
    _servicedb.close()


def getservices():
    return _servicedb.keys()

    
def getservice(sourceurl):
    d = _servicedb.get(sourceurl)
    if d:
        data = loads(d)
        if data.keys() != ["feedinfo", "config"] and data.keys() != ["config", "feedinfo"]:
            # convert old data from db
            data = {"feedinfo": data,
                    "config": {"publicname": data.get("title", "-none-"),
                               "privatename": data.get("title", "-none-"),
                               "publiclink": data.get("link"),
                               "fetchhowoften": 60}}
        # check and fix some errors
        if "publicname" not in data["config"]:
            data["config"]["publicname"] = data["feedinfo"].get("title", "-none-")
        if "privatename" not in data["config"]:
            data["config"]["privatename"] = data["config"].get("publicname", "-none-")
        if "publiclink" not in data["config"]:
            data["config"]["publiclink"] = data["feedinfo"].get("link", "-none-" )
            
        return data
    else:
        # new entry
        return {"feedinfo": {"TVsourceurl": sourceurl, "TVcreated": mx.DateTime.now()},
                "config": {}}

def getserviceflat(sourceurl):
    data = getservice(sourceurl)
    ret = data["feedinfo"]
    ret.update(data["config"])
    return ret

def getfeedinfo(sourceurl):
    return getservice(sourceurl)["feedinfo"]


def getconfig(sourceurl):
    return getservice(sourceurl)["config"]

def saveservice(service):
    d = dumps(service)
    _servicedb.put(key=service["feedinfo"]["TVsourceurl"], data=d), # , flags=db.DB_NOOVERWRITE)    


writelock = threading.Lock()

def savefeedinfo(feedinfo):
    writelock.acquire()
    saveservice({"feedinfo": feedinfo, "config": getconfig(feedinfo["TVsourceurl"])})
    writelock.release()
    

def saveconfig(sourceurl, config):
    writelock.acquire()
    saveservice({"feedinfo": getfeedinfo(sourceurl), "config": config})
    writelock.release()

feedinfo_cachetime = 0
feedinfo_cache = None

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
        y = getservice(x)
        config = y["config"]
        feedinfo = y["feedinfo"]
        title = config.get("publicname", feedinfo.get("title", "Unknown title for: %s" % x))
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

def issubscribed(serviceurl):
    return serviceurl in getsubscriptions()
                               

def subscribe(serviceurl):
    subscriptions = getsubscriptions()
    if serviceurl not in subscriptions:
        subscriptions.append(serviceurl)
        savesubscriptions(subscriptions)

def unsubscribe(serviceurl):
    subscriptions = getsubscriptions()
    if serviceurl not in subscriptions:
        return None
    else:
        newsub = []
        for x in subscriptions:
            if x != serviceurl:
                newsub.append(x)
        savesubscriptions(subscriptions)

init()
