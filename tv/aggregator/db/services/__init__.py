# DB functions for services (RSS feeds)

# Try using cPickle and cStringIO if available.

try:
    from cPickle import load, dump, loads, dumps
except ImportError:
    from pickle import load, dump, loads, dumps
    
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import mx.DateTime, mx.DateTime.Parser
                                
import os.path, atexit
from bsddb3 import db
import mx.DateTime
import tv.config
from tv.aggregator.db import _dbenv

# try loading dupdeb
def init():
    global _servicedb

    # create and open the DB
    _servicedb = db.DB(_dbenv)
    _servicedb.open("services",   
                    dbtype = db.DB_BTREE,
                    flags = db.DB_CREATE|db.DB_DIRTY_READ|db.DB_THREAD,
                    mode = 0644)
    atexit.register(close)

def getservicelist():
    return _servicedb.keys()
    
def getservice(sourceurl):
    d = _servicedb.get(sourceurl)
    if d:
        return loads(d)
    else:
        return {"TVsourceurl": sourceurl, "TVcreated": mx.DateTime.now()}

def saveservice(service):
    d = dumps(service)
    _servicedb.put(key=service["TVsourceurl"], data=d), # , flags=db.DB_NOOVERWRITE)    

def close():
    print "servicedb shutdown"
    _servicedb.close()


init()
