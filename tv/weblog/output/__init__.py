import os, os.path
import calendar
import re
import time
import string
import mx.DateTime

import tv.weblog.db
from tv.weblog.output import todo
from Cheetah.Template import Template

import tv.tools

import templates.calendar
import templates.daypage
import templates.guidpage
import templates.indexpage
import templates.item
import templates.monthpage
import templates.rss
import templates.sidebar

from pprint import pprint

calendar.setfirstweekday(0) #start day  Mon(0)-Sun(6)

guidpagespath = '/Users/md/Sites/md.hudora.de/blog/guids'
blogdirbase = '/Users/md/Sites/md.hudora.de/blog/'

# url handling

def filenameToUrl(filename):
    if filename:
        return filename.replace('/Users/md/Sites/md.hudora.de/blog', 'http://md.hudora.de/blog')
    
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

def getIndexPageFilename(category=None):
    return os.path.join(getCategoryPath(category), "index.html")

def getIndexPageUrl(category=None):
    return filenameToUrl(getIndexPageFilename(category))

def getRssPageFilename(category=None):
    return os.path.join(getCategoryPath(category), "rss.xml")

def getRssPageUrl(category=None):
    return filenameToUrl(getRssPageFilename(category))

def getMonthPageUrl(date, category=None):
    if date:
        return filenameToUrl(getMonthPageFilename(date, category))
    else:
        return '<unset>'

def getRelativePath(top, fromp):
    return top
    #XXX
    if fromp and top:
        if fromp == top:
            return top
        fromp = os.path.normpath(fromp)
        top = os.path.normpath(top)
        prefix = os.path.commonprefix([fromp, top])
        path = top[len(prefix):]
        levels = len(fromp[len(prefix):].split('/')) - 1
        #print fromp
        #print top
        #print "%s%s" % ('../' * levels, path)
        #print 
        return "%s%s" % ('../' * levels, path)
    return top

# templates

templateCache = {}

        
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

    if 'source' in ns:
        ns['source'] = tv.tools.descape(ns['source'])
    ns['text'] = tv.tools.descape(ns['text'])
    ns['title'] = tv.tools.descape(ns['title'])
    ns['date'] = dateNamespace(item['date'])
    ns['guidpageurl'] = getRelativePath(getGuidPageUrl(item['guid']), filenameToUrl(thispage))
    ns['guidpagelink'] = '<a href="%s">%s</a>' % (ns['guidpageurl'], item['title'])
    ns['permalink'] = '<a href="%s">#</a>' % getGuidPageUrl(item['guid'])
    return ns

# widgets

def genCalendar(date=mx.DateTime.now(), category=None, thispage=None, nohighlight=0):
    daylinks = [''] * 32
    for day in range(1, date.days_in_month+1):
        if len(tv.weblog.db.getItemsAtDay(mx.DateTime.DateTime(date.year, date.month, day), category)) > 0:
            daylinks[day] = getRelativePath(getDayPageUrl(mx.DateTime.DateTime(date.year, date.month, day)),
                                            filenameToUrl(thispage))
        else:
            daylinks[day] = ''

    previousmonth = tv.weblog.db.getPreviousMonthWithItems(date)
    nextmonth = tv.weblog.db.getNextMonthWithItems(date)

    calendarTemplate = templates.calendar.calendar(searchList=[
        {'weeklist': calendar.monthcalendar(date.year, date.month),
         'daynames': calendar.weekheader(2).split(' '),
         'date': dateNamespace(date),
         'daylinks': daylinks,
         'nohighlight': nohighlight,
         'monthpageurl': getRelativePath(getMonthPageUrl(date, category),
                                         filenameToUrl(thispage)),
         'previousmonthurl': getRelativePath(getMonthPageUrl(previousmonth),
                                             filenameToUrl(thispage)),
         'previousmonth': previousmonth,
         'nextmonthurl': getRelativePath(getMonthPageUrl(nextmonth),
                                         filenameToUrl(thispage)),
         'nextmonth': nextmonth,
         'thisday': date.day }])

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

# from xmlrpclib (effbot)
def escape(s, replace=string.replace):
    s = replace(s, "&", "&amp;")
    s = replace(s, "<", "&lt;")
    return replace(s, ">", "&gt;",)


# rendering

def renderItem(item):
    renderGuidPage(item)
    # first make it right, then make it fast ...
    #s = time.time()
    #renderDayPage(item['date'])
    #print "renderDayPage()\t%.2f" % (time.time() - s)
    #s = time.time()
    #renderMonthPage(item['date'])
    #print "renderMonthPage()\t%.2f" % (time.time() - s)

def renderGuidPage(item):

    s = time.time()
    thispage = getGuidPageFilename(item['guid'])

    ns = {'item': itemNamespace(item, thispage=thispage),
          'pagetype': 'guidpage',
          'daypage': getRelativePath(getDayPageFilename(item['date']), thispage),
          'escape': escape,
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          'calendar': genCalendar(item['date'], thispage=thispage)}

    previousGuid = tv.weblog.db.getPreviousItem(item)
    nextGuid = tv.weblog.db.getNextItem(item)
    if previousGuid:
        previousItem = tv.weblog.db.getItem(previousGuid)
        ns['previousitem'] = itemNamespace(previousItem)
        ns['previousitemlink'] = '<a href="%s">&lt;&lt; %s</a>' % (getRelativePath(getGuidPageUrl(previousItem['guid']),
                                                                   getGuidPageUrl(item['guid'])),
                                                                   previousItem['title'])
    else:
        ns['previousitem'] = None
        ns['previousitemlink'] = ''

    if nextGuid:
        nextItem = tv.weblog.db.getItem(nextGuid)
        ns['nextitem'] = itemNamespace(nextItem)
        ns['nextitemlink'] = '<a href="%s">%s &gt;&gt;</a>' % (getRelativePath(getGuidPageUrl(nextItem['guid']),
                                                               getGuidPageUrl(item['guid'])),
                                                               nextItem['title'])
        
    else:        
        ns['nextitem'] = None
        ns['nextitemlink'] = ''

    sidebarTemplate = templates.sidebar.sidebar(searchList=[ns])
    pageTemplate =  templates.guidpage.guidpage(searchList=[ns, {'sidebar': str(sidebarTemplate)}])

    # check dependencies
    for category in (item['categories'].keys() + [None]):
        if not os.path.exists(thispage) and tv.weblog.db.getItemsAtDay(item['date'], category) == 1:
            # first time we have a item at this day - all pages of this month need rerendering
            todo.addWholeMonth(item['date'], category)
        else:
            todo.addDayPage(item['date'], category)
            todo.addMonthPage(item['date'], category)
    if not os.path.exists(thispage):
        if previousGuid:
            todo.addGuidPage(previousGuid)
        if nextGuid:
            todo.addGuidPage(nextGuid)

    fp = open(ensurePath(thispage), 'w')
    fp.write(str(pageTemplate))
    fp.close()
    print "renderGuidPage(%s) \t%.2f" % (item['guid'], time.time() - s)
    

def renderDayPage(date, category=None):
    """Render the category or main page for a certain day of the year"""

    s = time.time()
    
    thispage = getDayPageFilename(date, category)
 
    itemlist = []
    for guid in tv.weblog.db.getItemsAtDay(date, category):
        item = tv.weblog.db.getItem(guid)
        ns = {'pagetype': 'daypage',
              'item': itemNamespace(item, thispage=thispage)}
        itemTemplate = templates.item.item(searchList=[ns])
        #print "   ", category, item['title'], item['date'], ns['item']['title']
        ns['rendered'] = str(itemTemplate)

        itemlist.append(ns)

    # no empty pages
    if len(itemlist) == 0:
        return

    ns = {'itemlist': itemlist,
          'date': dateNamespace(date),
          'daypage': getRelativePath(getDayPageUrl(date), filenameToUrl(thispage)),
          'monthpage': getRelativePath(getMonthPageUrl(date), filenameToUrl(thispage)),
          'escape': escape,
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          #'previousitemlink': '',
          #'nextitemlink': '',
          'calendar': genCalendar(date, category=category,
                                  thispage=thispage)}

    sidebarTemplate = templates.sidebar.sidebar(searchList=[ns])
    pageTemplate =  templates.daypage.daypage(searchList=[ns, {'sidebar': str(sidebarTemplate)}])

    # check dependencies
    if not os.path.exists(thispage):
        # all pages of this month need rerendering
        todo.addWholeMonth(date, category)
    else:
        todo.addMonthPage(date, category)

    fp = open(ensurePath(thispage), 'w')
    fp.write(str(pageTemplate))
    fp.close()
    print "renderDayPage(%s, %s)\t%.2f" % (str(date), category, time.time() - s)


def renderMonthPage(date, category=None):
    """Render the month overview page for a certain Month"""
    
    s = time.time()
    thispage = getMonthPageFilename(date, category)


    daylist = []
    for day in range(1, date.days_in_month+1):
        thisday = mx.DateTime.DateTime(date.year, date.month, day)
        dayitems = tv.weblog.db.getItemsAtDay(thisday, category)
        if not dayitems:
            continue

        itemlist = []
        for guid in dayitems:
            ns = {'pagetype': 'monthpage',
                  'item': itemNamespace(tv.weblog.db.getItem(guid), thispage=thispage)}
            itemTemplate = templates.item.item(searchList=[ns])
            ns['rendered'] = str(itemTemplate)
            itemlist.append(ns)

        daylist.append({'itemlist': itemlist,
                        'daypage': getRelativePath(getDayPageUrl(thisday), filenameToUrl(thispage)),
                        'date': dateNamespace(thisday)})

    # no empty pages
    if len(daylist) == 0:
        return
    
    ns = {'daylist': daylist,
          'date': dateNamespace(date),
          'escape': escape,
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          #'previousitemlink': '',
          #'nextitemlink': '',
          'calendar': genCalendar(date, category=category,
                                  thispage=thispage, nohighlight=1)}

    sidebarTemplate = templates.sidebar.sidebar(searchList=[ns])
    pageTemplate =  templates.monthpage.monthpage(searchList=[ns, {'sidebar': str(sidebarTemplate)}])

    # check dependencies
    if not os.path.exists(thispage):
        todo.addWholeMonth(tv.weblog.db.getPreviousMonthWithItems(date), category)
        todo.addWholeMonth(tv.weblog.db.getNextMonthWithItems(date), category)
     
    fp = open(ensurePath(thispage), 'w')
    fp.write(str(pageTemplate))
    fp.close()

    print "renderMonthPage(%s, %s)\t%.2f" % (str(date), category, time.time() - s)


def renderIndexPage(category=None):

    s = time.time()
    thispage = getIndexPageFilename(category)
    rsspage = getRssPageFilename(category)

    maxdays = 14
    maxitems = 20
    stopdate = mx.DateTime.DateTime(1990)
    
    noofitems = 0
    thisday = mx.DateTime.now() + 1
    daylist = []
    while len(daylist) <= maxdays and noofitems <= maxitems and thisday > stopdate:
        thisday = thisday - 1
        dayitems = tv.weblog.db.getItemsAtDay(thisday, category)
        if not dayitems:
            continue
        dayitems.reverse()

        itemlist = []
        for guid in dayitems:
            noofitems += 1
            ns = {'pagetype': 'indexpage',
                  'item': itemNamespace(tv.weblog.db.getItem(guid), thispage=thispage)}
            itemTemplate = templates.item.item(searchList=[ns])
            ns['rendered'] = str(itemTemplate)
            itemlist.append(ns)

        daylist.append({'itemlist': itemlist,
                        'daypage': getRelativePath(getDayPageUrl(thisday), filenameToUrl(thispage)),
                        'date': dateNamespace(thisday)})
        
        
    ns = {'daylist': daylist,
          'date': dateNamespace(mx.DateTime.now()),
          'escape': escape,
          #'googleit': 'unset',
          #'trackback': 'unset',
          #'translate': 'unset',
          #'previousitemlink': '',
          #'nextitemlink': '',
          'calendar': genCalendar(mx.DateTime.now(), category=category,
                                  thispage=thispage, nohighlight=1)}

    sidebarTemplate = templates.sidebar.sidebar(searchList=[ns])
    rssTemplate =  templates.rss.rss(searchList=[ns])
    pageTemplate =  templates.indexpage.indexpage(searchList=[ns, {'sidebar': str(sidebarTemplate)}])

     
    fp = open(ensurePath(rsspage), 'w')
    fp.write(str(rssTemplate))
    fp.close()

    fp = open(ensurePath(thispage), 'w')
    fp.write(str(pageTemplate))
    fp.close()

    print "renderIndexPage(%s)\t%.2f, %s" % (category, time.time() - s, rsspage)

