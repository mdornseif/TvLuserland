import tv.weblog.output
import tv.weblog.db

from mx.DateTime import DateTime
from pprint import pprint

_guidPageQueue = {}
_dayPageQueue = {}
_monthPageQueue = {}



def addGuidPage(guid):
    _guidPageQueue[guid] = 1

def addDayPage(date, category):
    if date:
        if category not in _dayPageQueue:
            _dayPageQueue[category] = {}
        _dayPageQueue[category][DateTime(date.year, date.month, date.day)] = 1

def addMonthPage(date, category):
    if date:
        if category not in _monthPageQueue:
            _monthPageQueue[category] = {}
        _monthPageQueue[category][DateTime(date.year, date.month, 1)] = 1
    
def addWholeMonth(date, category):
    if date:
        for day in range(1, date.days_in_month+1):
            addDayPage(DateTime(date.year, date.month, day), category)
        addMonthPage(date, category)

def commit():
    global _guidPageQueue, _dayPageQueue, _monthPageQueue

    print "working todolist"

    for x in _guidPageQueue.keys():
        tv.weblog.output.renderGuidPage(tv.weblog.db.getItem(x))
    _guidPageQueue = {}

    for cat in _dayPageQueue.keys():
        print cat
        tv.weblog.output.renderIndexPage(cat)
        k = _dayPageQueue[cat].keys()
        k.sort()
        k.reverse()
        for x in k:
            tv.weblog.output.renderDayPage(x, cat)
    _dayPageQueue = {}

    for cat in _monthPageQueue.keys():
        k = _monthPageQueue[cat].keys()
        k.sort()
        k.reverse()
        for x in k:
            tv.weblog.output.renderMonthPage(x, cat)
    _monthPageQueue = {}
    
