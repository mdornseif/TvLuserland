"""Get posts from Radio Userland by a mix of the metaWeblog API and
the blogger API.

--md@hudora.de
"""

import tv.config

def getPost(postid):
    return tv.config.getxmlrpcclient().metaWeblog.getPost(postid, tv.config.get("weblog.user"), tv.config.get("weblog.password"))

def getMaxPostId():
    return int(tv.config.getxmlrpcclient().blogger.getRecentPosts('','home', tv.config.get("weblog.user"), tv.config.get("weblog.password"), 1)[0]['postid'])

def getCategories():
    return tv.config.getxmlrpcclient().metaWeblog.getCategories('', tv.config.get("weblog.user"), tv.config.get("weblog.password"))

def newPost(post, publish = 1):
    return tv.config.getxmlrpcclient().metaWeblog.newPost('home', tv.config.get("weblog.user"), tv.config.get("weblog.password"), post, publish) 

def newDateForPost(postid, (year, month, day, hour, minute, seconds)):
    return tv.config.getxmlrpcclient().md.metaWeblog.newDateForPost(postid, tv.config.get("weblog.user"), tv.config.get("weblog.password"), year, month, day, hour, minute, seconds)

#metaWeblog.editPost (postid, username, password, struct, publish) returns true

#metaWeblog.getPost (postid, username, password) returns struct

