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
import time
from bsddb3 import db
import tv.config
from tv.aggregator.db import _dbenv

# try loading dupdeb
def init():
    global _dupedb, _itemdb, _itembysourcedb, _itembydatedb, _sourcedb

    # init dupedb
    try:
        fp = open(os.path.join(tv.config.get("fs.dbdir"), "items.dupedb.pickle"), 'r')
        _dupedb = load(fp)
        fp.close()
    except:
        _dupedb = {} 

    # init db
    # create and open the DB
    _itemdb = db.DB(_dbenv)
    _itemdb.open("items",   
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_DIRTY_READ|db.DB_THREAD,
                mode = 0644)

    # create secondary DBs
    _itembydatedb = db.DB(_dbenv)
    _itembydatedb.set_flags(db.DB_DUP)
    _itembydatedb.open("items-bydate",
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_DIRTY_READ|db.DB_THREAD,
                mode = 0644)
    _itembysourcedb = db.DB(_dbenv)
    _itembysourcedb.set_flags(db.DB_DUP)
    _itembysourcedb.open("items-bysource",   
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_DIRTY_READ|db.DB_THREAD,
                mode = 0644)
    atexit.register(close)


def getitem(guid):
    d = _itemdb.get(guid)
    return loads(d)

def getitemsBySource(sourceurl, maxitems = 0xffffffffffL):
    ret = []
    cur = _itembysourcedb.cursor()
    rec = cur.set(sourceurl)
    while rec:
        if len(ret) >= maxitems:
            break
        ret.append(getitem(rec[1]))
        rec = cur.next_dup()
    cur.close()
    return ret

def getitemsByDate(startdate = mx.DateTime.now(), maxitems = 50):
    ret = []
    cur = _itembydatedb.cursor()
    try:
        rec = cur.set_range(str(startdate))
    except db.DBNotFoundError:
        # this usually means that there is no newer element in the db, so start with the last one.
        rec = cur.last()
    while rec:
        if len(ret) >= maxitems:
            break
        ret.append(getitem(rec[1]))
        rec = cur.prev()
    return ret


def saveitem(item):
    d = dumps(item)
    _itemdb.put(key=item["guid"], data=d, flags=db.DB_NOOVERWRITE)
    _itembysourcedb.put(item["TVsourceurl"], item["guid"])
    _itembydatedb.put(key=str(item["TVdateobject"]), data=item["guid"])


def deleteitem(guid, date = None, sourceurl = None):
    """removes a item by deleting it from both helper databases but not from the main database.

    if you have item['TVdateobject'] and item['TVsourceurl'] you can
    give this to removeitem to speed things up."""
    
    item = getitem(guid)

    if date == None or sourceurl == None:
        item = getitem(guid)
        date = item["TVdateobject"]
        sourceurl = item["TVsourceurl"]

    try:
        cur = _itembydatedb.cursor()
        rec = cur.set_both(str(date), guid)
        cur.delete() 
        cur.close()
    except db.DBNotFoundError, msg:
        cur.close()
        print msg
        # something strange happened, we couldn't find this posting. We do
        # a full DB scan to find it's guid and remove it. ugly but effective.
        for k, v in _itembydatedb.items():
            cur = _itembydatedb.cursor()
            if v == guid:
                print "removing", k, guid
                rec = cur.set_both(k, guid)
                cur.delete() 
            cur.close()

    try:
        cur = _itembysourcedb.cursor()
        rec = cur.set_both(sourceurl, guid)    
        cur.delete()
        cur.close()
    except db.DBNotFoundError, msg:
        cur.close()
        print msg
        # something strange happened, we couldn't find this posting. We do
        # a full DB scan to find it's guid and remove it. ugly but effective.
        for k, v in _itembysourcedb.items():
            cur = _itembydatedb.cursor()
            if v == guid:
                print "removing", k, guid
                rec = cur.set_both(k, guid)
                cur.delete() 
            cur.close()
            

def save():
    fp = open(os.path.join(tv.config.get("fs.dbdir"), "items.dupedb.pickle"), 'w')
    dump(_dupedb, fp, 1)
    fp.flush()
    fp.close()

def close():
    save()
    _itemdb.close()
    _itembysourcedb.close()
    _itembydatedb.close()
    #_dbenv.close()

def checkdupe(item):
    if item["guid"] in _dupedb:
        ret = 1
    else:
        ret = None
    _dupedb[item["guid"]] = time.time()
    return ret


init()
