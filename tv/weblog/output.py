import os, os.path
import calendar
import re
import mx.DateTime

import tv.weblog.db
from Cheetah.Template import Template

from pprint import pprint

calendar.setfirstweekday(0) #start day  Mon(0)-Sun(6)

guidpagespath = '/Users/md/Sites/md.hudora.de/blog/guids'
blogdirbase = '/Users/md/Sites/md.hudora.de/blog/'

# url handling

def filenameToUrl(filename):
    if filename:
        return "http:/%s" % filename
    
def guidToFilename(guid):
    return os.path.join(guid[0:2], guid[2:4], guid[4:])

def getGuidPageFilename(guid):
    return os.path.join(guidpagespath, "%s.html" % guidToFilename(guid))

def getGuidPageUrl(guid):
    return filenameToUrl(getGuidPageFilename(guid))

def getCategoryPath(category):
    # XXX category != caterorypath!!!
    if category == None:
        return blogdirbase
    return os.path.join(blogdirbase, 'categories', category)

def getDayPageFilename(date, category=None):
    return os.path.join(getCategoryPath(category), "%d/%02d/%02d.html" % (date.year, date.month, date.day))

def getDayPageUrl(date, category=None):
    return filenameToUrl(getDayPageFilename(date, category))

def getMonthPageFilename(date, category=None):
    return os.path.join(getCategoryPath(category), "%d/%02d/overview.html" % (date.year, date.month))

def getMonthPageUrl(date, category=None):
    return filenameToUrl(getMonthPageFilename(date, category))

def getRelativePath(top, fromp):
    if fromp and top:
        if fromp == top:
            return top
        fromp = os.path.normpath(fromp)
        top = os.path.normpath(top)
        prefix = os.path.commonprefix([fromp, top])
        path = top[len(prefix):]
        levels = len(fromp[len(prefix):].split('/')) - 1
        return "%s%s" % ('../' * levels, path)
    return top

# templates

def readtemplate(name, subtemplate=0):
    """Reads the Template assosiated with id from disk, initializes
    it with the standard namespace and returns an template object"""

    if not subtemplate == 1:
        return Template(file="templates/%s.html" % (name), searchList=[])
    else:
        fd = open("templates/%s.html" % (name))
        html = fd.read()
        fd.close()
        return Template(source=stripHtmlHead(html), searchList=[])
        
def dateNamespace(date):
    ns = {}
    ns['day'] = date.day
    ns['day_of_week'] = date.day_of_week
    ns['day_of_year'] = date.day_of_year
    ns['hour'] = date.hour
    ns['iso_week'] = date.iso_week
    ns['minute'] = date.minute
    ns['month'] = date.month
    ns['second'] = date.second
    ns['strftime'] = date.strftime
    ns['year'] = date.year

    ns['arpadate'] = date.Format()
    ns['compact'] = str(date)[:16]
    ns['compactdate'] = str(date)[:10]
    ns['compacttime'] = str(date)[11:16]
    ns['isodate'] = str(date)
    ns['long'] = date.strftime("%A, %d. %B %Y, %H:%M:%S")
    ns['longdate'] = date.strftime("%A, %d. %B %Y")
    ns['longtime'] = str(date)[11:]
    return ns

def itemNamespace(item, thispage=None):
    ns = {'title': None, 'text': None}
    ns.update(item)
    
    ns['date'] = dateNamespace(item['date'])
    ns['guidpageurl'] = getRelativePath(getGuidPageUrl(item['guid']), filenameToUrl(thispage))
    ns['guidpagelink'] = '<a href="%s">%s</a>' % (ns['guidpageurl'], item['title'])
    ns['permalink'] = '<a href="%s">#</a>' % getGuidPageUrl(item['guid'])
    return ns

# widgets

def genCalendar(date=mx.DateTime.now(), category=None, thispage=None):
    daylinks = [''] * 32
    for day in range(1, date.days_in_month+1):
        if len(tv.weblog.db.getItemsAtDay(mx.DateTime.DateTime(date.year, date.month, day), category)) > 0:
            daylinks[day] = getRelativePath(getDayPageUrl(mx.DateTime.DateTime(date.year, date.month, day)),
                                            filenameToUrl(thispage))

        else:
            daylinks[day] = ''

    previousmonth = tv.weblog.db.getPreviousMonthWithItems(date)
    nextmonth = tv.weblog.db.getNextMonthWithItems(date)

    calendarTemplate = readtemplate('calendar', subtemplate=1)
    calendarTemplate.addToSearchList({'weeklist': calendar.monthcalendar(date.year, date.month),
                                      'daynames': calendar.weekheader(2).split(' '),
                                      'date': dateNamespace(date),
                                      'daylinks': daylinks,
                                      'previousmonthurl': getRelativePath(getMonthPageUrl(previousmonth),
                                                                          filenameToUrl(thispage)),
                                      'previousmonth': previousmonth,
                                      'nextmonthurl': getRelativePath(getMonthPageUrl(nextmonth),
                                                                      filenameToUrl(thispage)),
                                      'nextmonth': nextmonth,
                                      'thisday': date.day })
    return str(calendarTemplate)
                                                

# tools

def ensurePath(filename):
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    return filename

stripHtmlHead_re = re.compile(r'<body>(.*)</body>', re.IGNORECASE|re.DOTALL)
def stripHtmlHead(html):
    m = stripHtmlHead_re.search(html)
    return m.group(1).strip()

# rendering

def renderItem(item):
    import time
    s = time.time()
    renderGuidPage(item)
    print "renderGuidPage()\t%.2f" % (time.time() - s)
    # first make it right, then make it fast ...
    s = time.time()
    renderDayPage(item['date'])
    print "renderDayPage()\t%.2f" % (time.time() - s)
    for cat in item['categories']:
        s = time.time()
        renderDayPage(item['date'], cat)
        print "renderDayPage(%s)\t%.2f" % (cat, time.time() - s)

def renderGuidPage(item):
    thispage = getGuidPageFilename(item['guid'])
    fp = open(ensurePath(thispage), 'w')
    pageTemplate = readtemplate('guidpage')
    sidebarTemplate = readtemplate('sidebar', subtemplate=1)

    ns = {'item': itemNamespace(item, thispage=thispage),
          'pagetype': 'guidpage',
          'daypage': getRelativePath(getDayPageFilename(item['date']), thispage),
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          'calendar': genCalendar(item['date'], thispage=thispage)}

    
    (previousGuid, nextGuid) = tv.weblog.db.getSorrundingItems(item['guid'])
    if previousGuid:
        previousItem = tv.weblog.db.getItem(previousGuid)
        ns['previousitem'] = itemNamespace(previousItem)
        ns['previousitemlink'] = '<a href="%s">&lt;&lt; %s</a>' % (getRelativePath(getGuidPageFilename(previousItem['guid']),
                                                                   getGuidPageFilename(item['guid'])),
                                                                   previousItem['title'])
    if nextGuid:
        nextItem = tv.weblog.db.getItem(nextGuid)
        ns['nextitem'] = itemNamespace(nextItem)
        ns['nextitemlink'] = '<a href="%s">%s &gt;&gt;</a>' % (getRelativePath(getGuidPageFilename(nextItem['guid']),
                                                               getGuidPageFilename(item['guid'])),
                                                               nextItem['title'])

    sidebarTemplate.addToSearchList(ns)
    pageTemplate.addToSearchList(ns)
    pageTemplate.addToSearchList({'sidebar': str(sidebarTemplate)})
        
    #pprint(itemNamespace(item))
    fp.write(str(pageTemplate))
    fp.close()
    
def renderDayPage(date, category=None):
    """Render the category or main page for a certain day of the year"""
    
    thispage = getDayPageFilename(date, category)
    fp = open(ensurePath(thispage), 'w')
    pageTemplate = readtemplate('daypage')
    sidebarTemplate = readtemplate('sidebar', subtemplate=1)

    itemlist = []
    for guid in tv.weblog.db.getItemsAtDay(date, category):
        itemTemplate = readtemplate('item', subtemplate=1)
        ns = {'pagetype': 'daypage',
              'item': itemNamespace(tv.weblog.db.getItem(guid), thispage=thispage)}
        itemTemplate.addToSearchList(ns)
        itemlist.append(str(itemTemplate))

    ns = {'itemlist': itemlist,
          'date': dateNamespace(date),
          'daypage': '<blink>unset</blink>',
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          #'previousitemlink': '',
          #'nextitemlink': '',
          'calendar': genCalendar(date, category=category,
                                  thispage=thispage)}

    sidebarTemplate.addToSearchList(ns)
    pageTemplate.addToSearchList(ns)
    pageTemplate.addToSearchList({'sidebar': str(sidebarTemplate)})

    fp.write(str(pageTemplate))
    fp.close()
