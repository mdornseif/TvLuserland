# Try using cPickle and cStringIO if available.

__rcsid__ = "$Id: __init__.py,v 1.7 2002/12/23 18:58:58 drt Exp $"

try:
    from cPickle import load, dump, loads, dumps
except ImportError:
    from pickle import load, dump, loads, dumps
    
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import mx.DateTime
                                
import os.path
import atexit
import time
import md5
from bsddb3 import db

import tv.config
from tv.aggregator.db import _dbenv

# try loading dupdeb
def init():
    global _dupedb, _dupetitledb, _dupelinkdb, _dupedescriptiondb, _itemdb, _itembysourcedb, _itembydatedb, _sourcedb, _deletedb

    # init dupedb
    _dupedb = db.DB(_dbenv)
    _dupedb.open("dupes",   
                 dbtype = db.DB_BTREE,
                 flags = db.DB_CREATE|db.DB_THREAD,
                 mode = 0644)
    _dupetitledb = db.DB(_dbenv)
    _dupetitledb.set_flags(db.DB_DUP)
    _dupetitledb.open("dupes-title",   
                      dbtype = db.DB_BTREE,
                      flags = db.DB_CREATE|db.DB_THREAD,
                      mode = 0644)
    _dupelinkdb = db.DB(_dbenv)
    _dupelinkdb.set_flags(db.DB_DUP)
    _dupelinkdb.open("dupes-link",   
                     dbtype = db.DB_BTREE,
                     flags = db.DB_CREATE|db.DB_THREAD,
                     mode = 0644)
    _dupedescriptiondb = db.DB(_dbenv)
    _dupedescriptiondb.set_flags(db.DB_DUP)
    _dupedescriptiondb.open("dupes-description",   
                 dbtype = db.DB_BTREE,
                 flags = db.DB_CREATE|db.DB_THREAD,
                 mode = 0644)

    # init db
    # create and open the DB
    _itemdb = db.DB(_dbenv)
    _itemdb.open("items",   
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_THREAD,
                mode = 0644)

    # create secondary DBs
    _itembydatedb = db.DB(_dbenv)
    _itembydatedb.set_flags(db.DB_DUP)
    _itembydatedb.open("items-bydate",
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_THREAD,
                mode = 0644)
    _itembysourcedb = db.DB(_dbenv)
    _itembysourcedb.set_flags(db.DB_DUP)
    _itembysourcedb.open("items-bysource",   
                dbtype = db.DB_BTREE,
                flags = db.DB_CREATE|db.DB_THREAD,
                mode = 0644)

    _deletedb = db.DB(_dbenv)
    _deletedb.open("deletedb",   
                   dbtype = db.DB_RECNO,
                   flags = db.DB_CREATE|db.DB_THREAD,
                   mode = 0644)

    atexit.register(close)

def close():
    _itemdb.close()
    _itembysourcedb.close()
    _itembydatedb.close()
    _deletedb.close()
    _dupetitledb.close()
    _dupelinkdb.close()
    _dupedescriptiondb.close()
    #_dbenv.close()


def getitem(guid):
    d = _itemdb.get(guid)
    if d == None:
        print "error reading item %r" % guid
        deleteitemfromdate_iterating(guid)
        deleteitemfromsource_iterating(guid)
        return {}
    else:
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

def getitemsByDate(startdate = mx.DateTime.now(), maxitems = 50, upwards = 1):
    ret = []
    cur = _itembydatedb.cursor()
    try:
        rec = cur.set_range(str(startdate))
    except db.DBNotFoundError:
        # this usually means that there is no newer element in the db, so start with the last one.
        if upwards:
            rec = cur.first()
        else:
            rec = cur.last()
    while rec:
        if len(ret) >= maxitems:
            break
        ret.append(getitem(rec[1]))
        if upwards:
            rec = cur.next()
        else:
            rec = cur.prev()
    return ret


def saveitem(item):
    d = dumps(item)
    _itemdb.put(key=item["guid"], data=d)#, flags=db.DB_NOOVERWRITE)
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

    _deletedb.append(guid)

    try:
        cur = _itembydatedb.cursor()
        rec = cur.set_both(str(date), guid)
        cur.delete() 
        cur.close()
    except db.DBNotFoundError, msg:
        cur.close()
        print msg
        deleteitemfromdate_iterating(guid)

    try:
        cur = _itembysourcedb.cursor()
        rec = cur.set_both(sourceurl, guid)    
        cur.delete()
        cur.close()
    except db.DBNotFoundError, msg:
        cur.close()
        print msg
        deleteitemfromsource_iterating(guid)

def deleteitemfromdate_iterating(guid):
    # something strange happened, we couldn't find this posting. We do
    # a full DB scan to find it's guid and remove it. ugly but effective.
    print guid
    cur = _itembydatedb.cursor()
    for k, v in _itembydatedb.items():
        if v == guid:
            print "removing", k, guid
            rec = cur.set_both(k, v)
            if rec:
                cur.delete() 
    cur.close()

def deleteitemfromsource_iterating(guid):
    # something strange happened, we couldn't find this posting. We do
    # a full DB scan to find it's guid and remove it. ugly but effective.
    cur = _itembydatedb.cursor()
    for k, v in _itembysourcedb.items():
        if v == guid:
            rec = cur.set_both(k, guid)
            print "removing", k, guid, rec
            if rec:
                cur.delete() 
    cur.close()


def deleteallitemsfromsource(sourceurl):
    # get guids of all items and remove them from itembysourcedb
    guidlist = {}
    cur = _itembysourcedb.cursor()
    rec = cur.set(sourceurl)
    while rec:
        _deletedb.append(rec[1])
        guidlist[rec[1]] = 1
        cur.delete()
        rec = cur.next_dup()
    cur.close()

    # find them in itembydatedb by iterating (!) and remove them there
    cur = _itembydatedb.cursor()
    for k, v in _itembydatedb.items():
        if v in guidlist:
            print "removing", k, v
            rec = cur.set_both(k, v)
            cur.delete()
            del guidlist[v]
    cur.close()
    
def getnrofunreaditems():
    # DB_FAST_STAT ???
    return _itembydatedb.stat()["ndata"]

def getnrofunreaditemsforsource(sourceurl):
    ret = 0
    cur = _itembysourcedb.cursor()
    try:
        rec = cur.set(sourceurl)
    except db.DBNotFoundError:
        rec = None
    while rec:
        ret += 1
        rec = cur.next_dup()
    cur.close()
    return ret

def checkdupe(item):
    if _dupedb.has_key(item["guid"]):
        ret = 1
    else:
        ret = None
        _dupedb.put(key=item["guid"], data=str(mx.DateTime.now()))
        if "title" in item:
            _dupetitledb.put(key=str(item["title"]), data=item["guid"])
        if "link" in item:
            _dupelinkdb.put(key=str(item["link"]), data=item["guid"])
        if item.get("description", "").strip() != "":
            _dupedescriptiondb.put(key=md5.new(item["description"]).digest(), data=item["guid"])
    return ret

def applydeletelog():
    dlist = {}
    for x in _deletedb.values():
        dlist[x] = 1
    for k, v in _itembydatedb.items():
        if v in dlist:
            print v
            deleteitem(v)

def removeunreaddupes():
    cur = _itembydatedb.cursor()
    seenguids = {}
    for k, v in _itembydatedb.items():
        if v in seenguids:
            rec = cur.set_both(k, v)
            print "removing", k, v, rec
            if rec:
                cur.delete() 
        else:
            seenguids[v] = 1
    cur.close()
    
init()
