# -*- Mode: Python -*-

# See http://www.xml-rpc.com/
#     http://www.pythonware.com/products/xmlrpc/

# Based on "xmlrpcserver.py" by Fredrik Lundh (fredrik@pythonware.com)

VERSION = "$Id: xmlrpc_handler.py,v 1.3 2002/12/29 20:00:05 drt Exp $"

import xmlrpclib
import sys, traceback


import string
import sys

class xmlrpc_handler:

    def match (self, request):
        # Note: /RPC2 is not required by the spec, so you may override this method.
        if request.uri[:5] == '/RPC2':
            return 1
        else:
            return 0

    def handle_request (self, request):
        [path, params, query, fragment] = request.split_uri()

        if request.command in ('post', 'put'):
            request.collector = collector (self, request)
        else:
            request.error (400)

    def continue_request (self, data, request):            
        params, method = xmlrpclib.loads (data)
        try:
            # generate response
            try:
                response = self.call (method, params)
                if type(response) != type(()):
                    response = (response,)
            except:
                # report exception back to server
                print "Exception in user code:"
                print '-' * 60
                traceback.print_exc(file=sys.stdout)
                print '-' * 60
                                        
                response = xmlrpclib.dumps (
                        xmlrpclib.Fault (1, "%s:%s" % (sys.exc_type, sys.exc_value))
                        )
            else:
                response = xmlrpclib.dumps (response, methodresponse=1)
        except:
            # internal error, report as HTTP server error
            print "Exception in user code:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            request.error (500)
        else:
            # got a valid XML RPC response
            request['Content-Type'] = 'text/xml'
            request.push (response)
            request.done()

    def call (self, method, params):
        # override this method to implement RPC methods
        raise "NotYetImplemented"

class collector:

    "gathers input for POST and PUT requests"

    def __init__ (self, handler, request):

        self.handler = handler
        self.request = request
        self.data = ''

        # make sure there's a content-length header
        cl = request.get_header ('content-length')

        if not cl:
            request.error (411)
        else:
            cl = string.atoi (cl)
            # using a 'numeric' terminator
            self.request.channel.set_terminator (cl)

    def collect_incoming_data (self, data):
        self.data = self.data + data

    def found_terminator (self):
        # set the terminator back to the default
        self.request.channel.set_terminator ('\r\n\r\n')
        self.handler.continue_request (self.data, self.request)

#import xmlrpc_handler

#class rpc_demo (xmlrpc_handler):
#
#    def call (self, method, params):
#        print 'method="%s" params=%s' % (method, params)
#        return "Sure, that works"


if __name__ == '__main__':

    import http_server
    import asyncore

    hs = http_server.http_server ('', 8000)
    rpc = rpc_demo()
    hs.install_handler (rpc)

    asyncore.loop()
