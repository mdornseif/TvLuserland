""" DB functions for services (RSS feeds)

Services are saved in a bsddb as a dictionary of dictionarys. the
first level of dicionary contains items related to different parts of
the aggregator. At the moment there are only two entries defined:
'feedinfo' and 'config'. feedinfo is only to be written by the thread
reading rss files from the network, 'config' is only to be written by the GUI. 

"""


# Try using cPickle and cStringIO if available.
try:
    from cPickle import load, dump, loads, dumps
except ImportError:
    from pickle import load, dump, loads, dumps
    
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

                                
import os.path, atexit
import threading
from bsddb3 import db
import mx.DateTime

import tv.config
from tv.aggregator.db import _dbenv

def init():
    global _servicedb

    # create and open the DB
    _servicedb = db.DB(_dbenv)
    _servicedb.open("services",   
                    dbtype = db.DB_BTREE,
                    flags = db.DB_CREATE|db.DB_DIRTY_READ|db.DB_THREAD,
                    mode = 0644)
    atexit.register(close)


def close():
    _servicedb.close()


def getservicelist():
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
        return data
    else:
        # new entry
        return {"feedinfo": {"TVsourceurl": sourceurl, "TVcreated": mx.DateTime.now()},
                "config": {}}


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


init()
