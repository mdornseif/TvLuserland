from __future__ import generators

import os, os.path
import dircache
import cPickle
import time
from mx.DateTime import DateTime, now

dbdir = 'db'
_cache = {}

#from config import *
from pprint import pprint

def getItem(itemid):
    """Read item defined by itemid from disk or deliver it from our cache"""
    if itemid in _cache.setdefault('items', {}):
        return _cache['items'][itemid]
    
    fn = os.path.join(dbdir, 'weblog', 'items', '%s.pickle' % itemid) 
    fd = open(fn, 'r')
    item = cPickle.load(fd)
    fd.close()
    _cache.setdefault('items', {})[itemid] = item 
    _cache.setdefault('days', {}).setdefault(DateTime(item['date'].year, item['date'].month, item['date'].day), {})[item['date']] = item['guid']
    _cache['olddestitem'] = min(_cache.get('olddestitem', now()), item['date'])
    _cache['newestitem'] = max(_cache.get('newestitem', now() - 10000), item['date'])
    if type(item['text']) != type('abc'):
        print "unicode attacks!", itemid
        item['text'] = item['text'].encode('latin1', 'replace')
        saveItem(itemid, item)
    if type(item['title']) != type('abc'):
        print "unicode attacks!", itemid
        item['title'] = item['title'].encode('latin1', 'replace')
        saveItem(itemid, item)
    return item


def getAllItems():
    for x in dircache.listdir(os.path.join(dbdir, 'weblog', 'items')):
        if x.endswith('.pickle'):
            item = getItem(x[:-7])
            yield item

def getAllItemsByDate():
    initDb()
    k = _cache['days'].keys()
    k.sort()
    k.reverse()
    for day in k:
        for x in _cache['days'][day]:
            item = getItem(_cache['days'][day][x])
        yield item
    

def saveItem(itemid, item):
    fn = os.path.join(dbdir, 'weblog', 'items', '%s.pickle' % itemid)
    fp = open(fn + '.tmp', 'w')
    cPickle.dump(item, fp)
    fp.close()
    os.rename(fn + '.tmp', fn)

def getCategories():
    global categories
    fn = os.path.join(dbdir, 'categories.pickle') 
    fp = open(fn, 'r')
    categories = cPickle.load(fp)
    return categories

def saveCategories():
    fn = os.path.join(dbdir, 'categories.pickle')
    fp = open(fn + '.tmp', 'w')
    cPickle.dump(categories, fp)
    fp.close()
    os.rename(fn + '.tmp', fn)
    log.debug('saved to %s', fn)


#def getRadio():
#    global categories
#    categories = radio.getCategories()
#    saveCategories()


# navigation

def getOldestItem(category=None):
    if category is not None:
        raise NotImplementedError
    initDb()
    return _cache['olddestitem']


def getNewestItem(category=None):
    if category is not None:
        raise NotImplementedError
    initDb()
    return _cache['newestitem']


def getPreviousItem(item):
    initDb()
    day = DateTime(item['date'].year, item['date'].month, item['date'].day)
    oldest = getOldestItem()
    if day in _cache['days'] and len(_cache['days'][day]) > 0:
        dayitems = _cache['days'][day]
        k = dayitems.keys()
        k.sort()
        i = k.index(item['date']) - 1
        if i > 0:
            return dayitems[k[i]]

    while day >= oldest:
        day = day - 1
        if day in _cache['days'] and len(_cache['days'][day]) > 0:
            dayitems = _cache['days'][day]
            k = dayitems.keys()
            k.sort()
            return dayitems[k[-1]] 
        
    return None


def getNextItem(item):
    initDb()
    day = DateTime(item['date'].year, item['date'].month, item['date'].day)
    newest = getNewestItem()
    if day in _cache['days'] and len(_cache['days'][day]) > 0:
        dayitems = _cache['days'][day]
        k = dayitems.keys()
        k.sort()
        i = k.index(item['date']) + 1
        if i < len(dayitems):
            return dayitems[k[i]]

    while day <= newest:
        day = day + 1
        if day in _cache['days'] and len(_cache['days'][day]) > 0:
            dayitems = _cache['days'][day]
            k = dayitems.keys()
            k.sort()
            return dayitems[k[0]]

    return None
        

def getPreviousDayWithItems(date, category=None):
    initDb()
    day = date - 1
    oldest = getOldestItem()
    while day >= oldest:
        if getItemsAtDay(day, category):
            return day
        day = day - 1

def getNextDayWithItems(date, category=None):
    initDb()
    day = date + 1
    newest = getNewestItem()
    while day <= newest:
        if getItemsAtDay(day, category):
            return day
        day = day + 1
            
def getPreviousMonthWithItems(date, category=None):
    return getPreviousDayWithItems(DateTime(date.year, date.month, 1), category) 
    
def getNextMonthWithItems(date, category=None):
    return getNextDayWithItems(DateTime(date.year, date.month, date.days_in_month), category) 

def getItemsAtDay(date, category=None):
    initDb()
    day = DateTime(date.year, date.month, date.day)
    if day not in _cache['days']:
        return []
    dayitems = _cache['days'][day]
    k = dayitems.keys()
    k.sort()
    ret = []
    for x in k:
        if (category is None) or (category in _cache['items'][dayitems[x]]['categories']):
            ret.append(dayitems[x])
    return ret



dbinitialized = 0

def initDb(reinit = 0):
    """Fill cache"""
     
    global dbinitialized
    
    if dbinitialized == 1 and reinit == 0:
        return

    for item in getAllItems():
        pass
    dbinitialized = 1
