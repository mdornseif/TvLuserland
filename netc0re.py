import asyncore

from tv.thirdparty.medusa import http_server
import tv.aggregator.db.services

class subscribe_handler:
    """Handeles RSS Seubscription Requests as recived by popular Weblog/Aggregator Software"""
    # Ampheta http://127.0.0.1:8888/index.html?add_url=
    # Radio http://127.0.0.1:5335/system/pages/subscriptions?url=
    # Headline Viewer: http://127.0.0.1:8900/add_provider?url=
    

    def match (self, request):
        path, params, query, fragment = request.split_uri()
        if path == "/index.html" and query.startswith('?add_url='):
            # Ampheta
            return 1
        if path == "/system/pages/subscriptions" and query.startswith('?url='):
            # Radio
            return 1
        if path == "/add_provider" and query.startswith('?url='):
            # Headline Viewer
            return 1
        return 0

    def handle_request (self, request):
        path, params, query, fragment = request.split_uri()
        serviceurl = query[query.find('url=')+4:]
        request['Content-Type'] = 'text/html'
        if tv.aggregator.db.services.issubscribed(serviceurl):
            request.push ('<html><title>TV Luserland</title><body>You are already subscribed to %r.</body></html>' % serviceurl)
        else:
            tv.aggregator.db.services.subscribe(serviceurl)
            request.push ('<html><title>TV Luserland</title><body>Subscribing you to %r.</body></html>' % serviceurl)                
        request.done()


    def status (self):
        import producers
        return producers.simple_producer ( '<li> RSS Subscription Handler')


##################################################


from tv.thirdparty.medusa import xmlrpc_handler
import xmlrpclib

# Some type names for use in method signatures.
INT="int"
BOOLEAN="boolean"
DOUBLE="double"
STRING="string"
DATETIME="dateTime.iso8601"
BASE64="base64"
ARRAY="array"
STRUCT="struct"

# Some error codes, borrowed from xmlrpc-c.
INTERNAL_ERROR = -500
TYPE_ERROR = -501
INDEX_ERROR = -502
PARSE_ERROR = -503
NETWORK_ERROR = -504
TIMEOUT_ERROR = -505
NO_SUCH_METHOD_ERROR = -506
REQUEST_REFUSED_ERROR = -507
INTROSPECTION_DISABLED_ERROR = -508
LIMIT_EXCEEDED_ERROR = -509
INVALID_UTF8_ERROR = -510


class xmlrpc_srv(xmlrpc_handler.xmlrpc_handler):
    
    def __init__ (self, allow_introspection=1):
        self._allow_introspection = allow_introspection
        self._methods = {}
        self._signatures = {}
        self._help = {}
        self._capabilities = {}
        self._default_method = None
        if allow_introspection:
            state = 'enabled'
        else:
            state = 'disabled'
        self._install_system_methods()
        self.add_capability('xmlrpc', 'http://www.xmlrpc.com/spec', 1)


    def _install_system_methods(self):
        self.add_method('system.listMethods',
                        self.system_listMethods,
                        [[ARRAY]])
        self.add_method('system.methodSignature',
                        self.system_methodSignature,
                        [[ARRAY, STRING]])
        self.add_method('system.methodHelp',
                        self.system_methodHelp,
                        [[STRING, STRING]])
        self.add_method('system.multicall',
                        self.system_multicall,
                        [[ARRAY, ARRAY]])
        self.add_method('system.getCapabilities',
                        self.system_getCapabilities,
                        [[STRUCT]])

    def add_method(self, name, method, signature=None, help=None):
        if help == None:
            help = method.__doc__
        if help == None:
            help = ''
        if signature == None:
            signature = 'undef'

        self._methods[name] = method
        self._signatures[name] = signature
        self._help[name] = help

    def add_capability(self, name, specUrl, specVersion):
        self._capabilities[name] = {
            'specUrl': str(specUrl),
            'specVersion': int(specVersion)
            }

    def set_default_method(self, method):
        self._default_method = method

    def _no_such_method(self, name):
    	raise xmlrpclib.Fault(NO_SUCH_METHOD_ERROR, "no such method: %r" % str(name))

    def _introspection_check(self):
    	if not self._allow_introspection:
            raise xmlrpclib.Fault(INTROSPECTION_DISABLED_ERROR,
                                  ("Introspection has been disabled on this server."))
    
    def system_listMethods(self):
    	self._introspection_check()
    	return self._methods.keys()

    def system_methodSignature(self, name):
    	self._introspection_check()
    	if self._signatures.has_key(name):
            return self._signatures[name]
    	else:
            self._no_such_method(name)

    def system_methodHelp(self, name):
    	self._introspection_check()
    	if self._help.has_key(name):
            return self._help[name]
    	else:
            self._no_such_method(name)

    def system_getCapabilities(self):
    	self._introspection_check()
    	return self._capabilities

    def system_multicall(self, calls):
    	results = []
    	for call in calls:
            # XXX: individual faults and exceptions are not logged
            # probable solution: move exception handling from do_POST to
            # dispatch_call
            try:
                name = call['methodName']
                params = call['params']
                if name == 'system.multicall':
                    errmsg = "Recursive system.multicall forbidden"
                    raise xmlrpclib.Fault(REQUEST_REFUSED_ERROR, errmsg)
                result = [self.dispatch_call(name, params)]
            except xmlrpclib.Fault, fault:
                result = {'faultCode': fault.faultCode,
                          'faultString': fault.faultString}
            except:
                info = sys.exc_info()
                errmsg = "%s:%s" % (info[0], info[1])
                result = {'faultCode': 1, 'faultString': errmsg}
            results.append(result)
    	return results

    def call(self, name, params):
        print 'method=%r params=%r' % (name, params)
        if self._methods.has_key(name):
            method = self._methods[name]
        else:
            method = self._default_method
        if method == None:
            self._no_such_method(name)
        ret = apply(method, params)
        if ret is None:
            ret = list(request.getpeername())
        return ret


class metaWeblog(xmlrpc_srv):
    
    def __init__ (self, allow_introspection=1):
        xmlrpc_srv.__init__(self, allow_introspection)
        self.add_method('metaWeblog.newPost', self.newPost,
                        [STRING, STRING, STRING, STRUCT, INT])
        self.add_method('metaWeblog.editPost', self.editPost,
                        [STRING, STRING, STRING, STRUCT, INT])
        self.add_method('metaWeblog.getPost', self.getPost,
                        [STRING, STRING, STRING])
        self.add_method('metaWeblog.getCategories', self.getCategories,
                        [STRING, STRING, STRING])
        self.add_method('metaWeblog.etRecentPosts', self.etRecentPosts,
                        [STRING, STRING, STRING, INT])

    
    def newPost(blogid, username, password, struct, publish):
        """newPost(blogid, username, password, struct, publish)

        Returns string representing the id of the new post. Keep in
        mind that this postid does not has to be numeric.

        'blogid' is ignored, 'username' and 'password' have an obvious
        purpose, and 'struct' is modelled after an RSS item.

        See http://www.xmlrpc.com/metaWeblogApi for further
        enligthenment."""

        pass

    def editPost(postid, username, password, struct, publish):
        """editPost(postid, username, password, struct, publish)

        Returns true.

        'postid' is id of the post to edit - e.g. returned by
        newPost(), 'username' and 'password' have an obvious purpose,
        and 'struct' is the same as in newPost(). Members set in
        'struct' overwrite the corrospondending values in the old
        posting. Other values in the old posting remain unchanged.

        See http://www.xmlrpc.com/metaWeblogApi for further
        enligthenment."""

        pass


    def getPost(postid, username, password):
        """getPost(postid, username, password), returns struct

        Returns a struct representing the posting with the id 'postid'. 

        See http://www.xmlrpc.com/metaWeblogApi for further
        enligthenment."""    
        pass
    

    def getCategories(blogid, username, password):
        """getCategories(postid, username, password)

        Returns a struct containing one struct for each category,
        containing the following elements: description, htmlUrl and
        rssUrl.

        See http://www.xmlrpc.com/metaWeblogApi for further
        enligthenment."""
        pass


    def getRecentPosts(blogid, username, password, howmany):
        """metaWeblog.getRecentPosts(blogid, username, password, howmany)
        
        Returns a list of the most recent posts in the system.
        
        Return value: on success, array of structs containing
        ISO.8601 dateCreated, String userid, String postid, String
        description, String title, String link, String permaLink,
        String mt_excerpt, String mt_text_more, boolean
        mt_allow_comments, boolean mt_allow_pings, boolean
        mt_convert_breaks; on failure, fault

        See
        http://www.movabletype.org/mt-static/docs/mtmanual_programmatic.html#item_metaWeblog%2EgetRecentPosts
        """
        pass
    

import asyncore

hs = http_server.http_server ('127.0.0.1', 8000)
rpc = metaWeblog()
hs.install_handler (rpc)

ah = subscribe_handler()
h1 = http_server.http_server('127.0.0.1', 8888)
h2 = http_server.http_server('127.0.0.1', 8900)
#h3 = http_server.http_server('127.0.0.1', 5335)
h1.install_handler (ah)
h2.install_handler (ah)
#h3.install_handler (ah)
asyncore.loop()

