# get bsddb environment for al our sub-modules

# Try using cPickle and cStringIO if available.
                                
import os.path
from bsddb3 import db
import tv.config

# try loading dupdeb
def init():
    global _dbenv
    try:
        os.makedirs(os.path.join(tv.config.get("fs.dbdir"), "bsddb"), 0755)
    except os.error: pass

    # init dbenv
    _dbenv = db.DBEnv()
    _dbenv.set_lg_max(1024*1024)
    _dbenv.open(os.path.join(tv.config.get("fs.dbdir"), "bsddb"),
                db.DB_CREATE | db.DB_THREAD | db.DB_INIT_MPOOL | db.DB_INIT_LOCK)

init()
