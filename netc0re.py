import asyncore

from tv.thirdparty.medusa import http_server
import tv.aggregator.db.services

class subscribe_handler:
    """Handeles RSS Seubscription rEquests as recived by popular Weblog/Aggregator Software"""
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


ah = subscribe_handler()
h1 = http_server.http_server('127.0.0.1', 8888)
h2 = http_server.http_server('127.0.0.1', 8900)
#h3 = http_server.http_server('127.0.0.1', 5335)
h1.install_handler (ah)
h2.install_handler (ah)
#h3.install_handler (ah)
asyncore.loop()

