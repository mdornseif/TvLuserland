from __future__ import generators

import os, os.path
import dircache
import cPickle
import time
from mx.DateTime import DateTime

dbdir = 'db'

#from config import *
from pprint import pprint

def getItem(itemid):
    fn = os.path.join(dbdir, 'weblog', 'items', '%s.pickle' % itemid) 
    fp = open(fn, 'r')
    return cPickle.load(fp)


def getAllItems():
    for x in dircache.listdir(os.path.join(dbdir, 'weblog', 'items')):
        if x.endswith('.pickle'):
            item = getItem(x[:-7])
        yield item

def getAllItemsByDate():
    initDb()
    k = bydateandcat[None].keys()
    k.sort()
    k.reverse()
    for x in k:
        item = getItem(bydateandcat[None][x])
        yield item
    

def saveItem(itemid, item):
    fn = os.path.join(dbdir, 'weblog', 'items', '%08d.pickle' % itemid)
    fp = open(fn + '.tmp', 'w')
    cPickle.dump(item, fp)
    fp.close()
    os.rename(fn + '.tmp', fn)
    log.debug('saved to %s', fn)

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

def getDateList(category=None):
    initDb()
    return datelist[category][:]

def getOldestItem(category=None):
    bydate = initDb()
    return bydate[category][min(bydate[category])]


def getNewestItem(category=None):
    bydate = initDb()
    return bydate[category][max(bydate[category])]


def getSorrundingItems(itemid, category=None):
    dates = getDateList(category)
    bydate = initDb()
    pos = dates.index(getItem(itemid)['date'])
    if pos < len(dates)-1:
        next =  bydate[category][dates[pos + 1]]
    else:
        next = None
    if pos > 0:
        previous = bydate[category][dates[pos - 1]]
    else:
        previous = None
    return (previous, next)


def getNextItem(itemid, category=None):
    return getSorrundingItems(itemid, category)[1]
    
    
def getPreviousItem(itemid, category=None):
    return getSorrundingItems(itemid, category)[0]


def getPreviousDayWithItems(day, category=None):
    thisday = day.day
    dates = getDateList(category)
    # seek the first item older
    while len(dates) > 0:
        x = dates.pop()
        if x < day:
            dates.append(x)
            break

    # seek the next item not on that day
    x = None
    while len(dates) > 0:
        x = dates.pop()
        if x.day != thisday:
            break

    return x


def getNextDayWithItems(day, category=None):
    thisday = day.day
    dates = getDateList(category)
    dates.reverse()
    # seek the first item younger
    while len(dates) > 0:
        x = dates.pop()
        if x > day:
            dates.append(x)
            break

    # seek the next item not on that day
    x = None
    while len(dates) > 0:
        x = dates.pop()
        if x.day != thisday:
            break

    return x
            
def getPreviousMonthWithItems(day, category=None):
    thismonth = day.month
    dates = getDateList(category)
    # seek the first item older
    while len(dates) > 0:
        x = dates.pop()
        if x < day:
            dates.append(x)
            break

    # seek the next item not on that day
    x = None
    while len(dates) > 0:
        x = dates.pop()
        if x.month != thismonth:
            break
        x = None

    return x
    
def getNextMonthWithItems(day, category=None):
    thismonth = day.month
    dates = getDateList(category)
    dates.reverse()
    # seek the first item younger
    while len(dates) > 0:
        x = dates.pop()
        if x > day:
            dates.append(x)
            break

    # seek the next item not on that day
    x = None
    while len(dates) > 0:
        x = dates.pop()
        if x.month != thismonth:
            break
        x = None
        
    return x


def getItemsAtDay(day, category=None):

    
    if (category in daylist) and (day in daylist[category]):
        return daylist[category][day].keys()   
    else:
        return []

    ### old stuff
    dates = getDateList(category)
    
    start = DateTime(day.year, day.month, day.day)
    end = start + 1

    # seek first item at that day
    while len(dates) > 0:
        x = dates.pop()
        if x < end:
            dates.append(x)
            break
    #laterdates = []
    #for x in dates:
    #    if x < end:
    #        laterdates = dates[dates.index(x):]
    #dates = laterdates

    # count items at the day
    guids = []
    bydate = initDb()
    while len(dates) > 0:
        x = dates.pop()
        if x < start:
            break
        guids.insert(-1, bydate[category][x])

    return guids


dbinitialized = 0
bydateandcat = {None: {}}
datelist = {}
daylist = {}

def initDb(reinit = 0):
     
    global bydateandcat, dbinitialized, datelist
    
    if dbinitialized == 1 and reinit == 0:
        return bydateandcat

    # XXX: this does not work out ... hmm ...
    # check if we can load from cache ... works at least on a Unix Filesystem
    #try:
    #    if os.path.getmtime(os.path.join(dbdir, 'weblog', 'items')) < os.path.getmtime(os.path.join(dbdir, 'weblog', 'ItemsByDate.pickle')):
    #        fd = open(os.path.join(dbdir, 'weblog', 'ItemsByDate.pickle'))
    #        x = cPickle.load(fd)
    #        dbinitialized = 1
    #        return x
    #except IOError:
    #    pass
    #except EOFError:
    #    pass
    #except OSError:
    #    pass
    
    for item in getAllItems():
        if item['date'] in bydateandcat[None]:
            print "Dupe!"
        bydateandcat[None][item['date']] = item['guid']
        if None not in daylist:
            daylist[None] = {}
        day = DateTime(item['date'].year, item['date'].month, item['date'].day)
        if day not in daylist[None]:
            daylist[None][day] = {}
        daylist[None][day][item['guid']] = 1   
        for x in item["categories"]:
            if x not in bydateandcat:
                bydateandcat[x] = {}
            bydateandcat[x][item['date']] = item['guid']
            if x not in daylist:
                daylist[x] = {}
            day = DateTime(item['date'].year, item['date'].month, item['date'].day)
            if day not in daylist[x]:
                daylist[x][day] = {}
            daylist[x][day][item['guid']] = 1   
    dbinitialized = 1

    for category in bydateandcat.keys():
        dates = bydateandcat[category].keys()
        dates.sort()
        datelist[category] = dates
    
    #fd = open(os.path.join(dbdir, 'weblog', 'ItemsByDate.pickle'), 'w')
    #cPickle.dump(bydateandcat, fd)
    #fd.close()
    return bydateandcat


#getRadio()

                
