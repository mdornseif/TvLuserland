
import cPickle

defaults = {"version": 1,
            "ui.newsitems": 23,
            "ui.deleteafterpost": 1,
            "ui.autopreview": 1,
            "weblog.user": "",
            "weblog.password": "",
            "weblog.server": "http://127.0.0.1:5335",
            "weblog.xmlrpcdebug": 0,
            "weblog.hasMetaWeblogApi": 1,
            "weblog.hasSetDate": 1,
            "weblog.hasAggregatorApi": 1,
            "fs.dbdir": "./db/",
            "net.timeout": 120
            }

_radioproxy = None
_lastserver = None
_lastverbose = None

# try loading configuration
_config = defaults.copy()
try:
    fp = open('.tvconfig.pickle', 'r')
    _config.update(cPickle.load(fp))
    fp.close()
except:
    pass


def get(key):
    return _config[key]

def set(key, value):
    _config[key] = value

def save():
    fp = open('.tvconfig.pickle', 'w')
    cPickle.dump(_config, fp)
    fp.flush()
    fp.close()


def getxmlrpcclient():
    import xmlrpclib, types
    global _radioproxy, _lastserver, _lastverbose
    
    if type(_radioproxy) == types.NoneType and _lastserver == get("weblog.server") and _lastverbose == get("weblog.xmlrpcdebug"):
        pass
    else:
        _radioproxy = xmlrpclib.Server(get("weblog.server"), verbose = get("weblog.xmlrpcdebug"))
        _lastserver = get("weblog.server")
        _lastverbose = get("weblog.xmlrpcdebug")
    return _radioproxy
