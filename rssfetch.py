#!/usr/local/bin/python



__rcsid__ = "$Id: rssfetch.py,v 1.6 2002/11/09 08:34:27 drt Exp $"

import rssparser
import random
import md5
import re
import htmlentitydefs
import mx.DateTime, mx.DateTime.Parser
import tv.aggregator.db.items
import tv.aggregator.db.services

from pprint import pprint

URLS = [
"http://80211b.weblogger.com/xml/rss.xml",
"http://BitStream.ManilaSites.Com/xml/rss.xml",
"http://Class6F.ManilaSites.Com/xml/rss.xml",
"http://archipelago.phrasewise.com/xml/rss.xml",
"http://blaeu.ManilaSites.Com/xml/rss.xml",
"http://blog.glennf.com/rss.xml",
"http://blognewsnetwork.com/members/0000012/rss.xml",
"http://blogs.it/0100198/rss.xml",
"http://blogs.salon.com/0001429/rss.xml",
"http://blogs.salon.com/0001444/rss.xml",
"http://blogspace.com/swhack/weblog/index.rss",
"http://boingboing.net/rss.xml",
"http://bpdg.blogs.eff.org/index.xml",
"http://bumppo.net/index.xml",
"http://buzz.weblogs.com/xml/rss.xml",
"http://christina.ManilaSites.Com/xml/rss.xml",
"http://coolstop.com/radio/rss.xml",
"http://db.cs.helsinki.fi/%7Ejajvirta/pythonowns.rss",
"http://deepblack.lolitacoders.org/~drt/rss/berkman.rss",
"http://deepblack.lolitacoders.org/~drt/rss/copyfight.rss",           
"http://deepblack.lolitacoders.org/~drt/rss/dud.rss",                 
"http://deepblack.lolitacoders.org/~drt/rss/greplaw.rss",             
"http://deepblack.lolitacoders.org/~drt/rss/isn.rss",                 
"http://deepblack.lolitacoders.org/~drt/rss/juristblogs.rss",
"http://deepblack.lolitacoders.org/~drt/rss/juristcfp.rss",       
"http://deepblack.lolitacoders.org/~drt/rss/juristconferences.rss",   
"http://deepblack.lolitacoders.org/~drt/rss/juristpositions.rss", 
"http://deepblack.lolitacoders.org/~drt/rss/juristwebcasts.rss",   
"http://deepblack.lolitacoders.org/~drt/rss/jurpc.rss",
"http://deepblack.lolitacoders.org/~drt/rss/newsfactor.rss",          
"http://deepblack.lolitacoders.org/~drt/rss/qdepesche.rss",
"http://deepblack.lolitacoders.org/~drt/rss/quicklinks.rss",         
"http://deepblack.lolitacoders.org/~drt/rss/quicklinkscc.rss",        
"http://deepblack.lolitacoders.org/~drt/rss/saverinternet-events.rss",
"http://deepblack.lolitacoders.org/~drt/rss/sicherheitiminternet.rss",
"http://deepblack.lolitacoders.org/~drt/rss/vnunet.rss",              
"http://degraaff.org/hci/hci-index.rdf",
"http://dijest.com/aka/categories/shrubbery/rss.xml",
"http://dijest.com/aka/rss.xml",
"http://dijest.editthispage.com/xml/rss.xml",
"http://disco.ucsd.edu/blog/?q=rss&flav=rss",
"http://diveintomark.org/xml/rss2.xml",
"http://doc.weblogs.com/xml/rss.xml",
"http://dws.us/weblog/rss.xml",
"http://excitedutterances.blogspot.com/rss/excitedutterances.xml",
"http://export.cnet.com/export/feeds/news/rss/1,11176,,00.xml",
"http://feed.rssengine.com/articlecentral.com/legalissues.rss",
"http://feed.rssengine.com/articlecentral.com/python.rss",
"http://feed.rssengine.com/articlecentral.com/security.rss",
"http://feed.rssengine.com/developerworks.com/security-articles.rss",
"http://feed.rssengine.com/eurekalert.org/policyethics.rss",
"http://feed.rssengine.com/eurekalert.org/technologyengineering.rss",
"http://feed.rssengine.com/gcn.com/dodcomputing.rss",
"http://feed.rssengine.com/gcn.com/egovernment.rss",
"http://feed.rssengine.com/gcn.com/homeland.rss",
"http://feed.rssengine.com/gcn.com/itstructure.rss",
"http://feed.rssengine.com/gcn.com/knowmgmt.rss",
"http://feed.rssengine.com/gcn.com/mobilewireless.rss",
"http://feed.rssengine.com/gcn.com/regulation.rss",
"http://feed.rssengine.com/gcn.com/sandl.rss",
"http://feed.rssengine.com/gcn.com/security.rss",
"http://feed.rssengine.com/upi.com/thinktanks.rss",
"http://fragen.editthispage.com/xml/rss.xml",
"http://gizmodo.net/index.rdf",
"http://google.blogspace.com/index.xml",
"http://grep.law.harvard.edu/greplaw.rss",
"http://headlines.internet.com/internetnews/ec-news/news.rss",
"http://headlines.internet.com/internetnews/fina-news/news.rss",
"http://headlines.internet.com/internetnews/intra-news/news.rss",
"http://headlines.internet.com/internetnews/isp-news/news.rss",
"http://headlines.internet.com/internetnews/prod-news/news.rss",
"http://headlines.internet.com/internetnews/streaming-news/news.rss",
"http://headlines.internet.com/internetnews/wd-news/news.rss",
"http://inessential.com/xml/rss.xml",
"http://instapundit.com/index.rdf",
"http://instructionaltechnology.editthispage.com/xml/rss.xml",
"http://jake.editthispage.com/xml/rss.xml",
"http://jarretthousenorth.editthispage.com/xml/rss.xml",
"http://jd.manilasites.com/xml/rss.xml",
"http://jeit.editthispage.com/xml/rss.xml",
"http://jeremy.zawodny.com/blog/index.rdf",
"http://joriss.jamby.net/xml/rss.xml",
"http://koeln.ccc.de/backend/headlines.rdf.php",
"http://krit.de/kritlog/rss.xml",
"http://lambda.weblogs.com/xml/rss.xml",
"http://lessig.org/index.rdf",
"http://macosx.weblogs.com/xml/rss.xml",
"http://members.aol.com/vitello/channelNS.rdf",
"http://members.tripod.com/smogzer/smog.rdf",
"http://msl1.mit.edu/furdlog/index.php?wl_mode=rss",
"http://myrss.com/f/b/l/blogspotZxykst2.rss91",
"http://neptune.he.net/~megarad/backend.php",
"http://news.openflows.org/newsviaopenflows.rdf",
"http://newsfeeds.manilasites.com/xml/rss.xml",
"http://newsround.ground-level.org/xml/rss.xml",
"http://organica.us/xml/organica.rdf",
"http://osx.macnn.com/osx.rdf",
"http://radio.weblogs.com/0001013/rss.xml",
"http://radio.weblogs.com/0001017/rss.xml",
"http://radio.weblogs.com/0001275/categories/war/rss.xml",
"http://radio.weblogs.com/0100059/rss.xml",
"http://radio.weblogs.com/0100190/categories/radioUserland/rss.xml",
"http://radio.weblogs.com/0100367/rss.xml",
"http://radio.weblogs.com/0100676/rss.xml",
#"http://radio.weblogs.com/0100887/categories/security/rss.xml",
#"http://radio.weblogs.com/0102677/categories/python/rss.xml",
#"http://radio.weblogs.com/0102677/rss.xml",
"http://radio.weblogs.com/0103069/rss.xml",
"http://radio.weblogs.com/0103213/rss.xml",
"http://radio.weblogs.com/0103705/categories/legalTechStandards/rss.xml",
"http://radio.weblogs.com/0103705/rss.xml",
"http://radio.weblogs.com/0104112/rss.xml",
"http://radio.weblogs.com/0104487/rss.xml",
"http://radio.weblogs.com/0104634/rss.xml",
"http://radio.weblogs.com/0105060/categories/securityPrivacyNews/rss.xml",
"http://radio.weblogs.com/0106129/rss.xml",
"http://radio.weblogs.com/0109773/rss.xml",
"http://radio.weblogs.com/0110436/rss.xml",
"http://radio.weblogs.com/0111972/rss.xml",
"http://research.yale.edu/lawmeme/backend.php",
"http://slashdot.org/apple.rdf",
"http://slashdot.org/books.rdf",
"http://slashdot.org/bsd.rdf",
"http://slashdot.org/interviews.rdf",
"http://slashdot.org/yro.rdf",
"http://static.userland.com/tomalak/links2.xml",
"http://static.userland.com/updatelogs/Radio.xml",
"http://tbtf.com/tbtf-userland.xml",
"http://thehacktivist.com/backend.php",
"http://themes.userland.com/xml/rss.xml",
"http://trainedmonkey.com/news/rss.php?s=11",
"http://udell.roninhouse.com/udell.rdf",
"http://usrlib.info/rss/backend.rdf",
"http://wmf.editthispage.com/xml/rss.xml",
"http://ww1.prweb.com/xml/legal.xml",
"http://www.PrivacyDigest.com/mostRecentNews",
"http://www.advogato.org/rss/articles.xml",
"http://www.andrewraff.com/index.rdf",
"http://www.bbc.co.uk/syndication/feeds/news/ukfs_news/technology/rss091.xml",
"http://www.benefitslink.com/rdf/benefitslink-courtcases.rdf",
"http://www.ccc.de/calendar/recent.rss",
"http://www.ccc.de/updates/recent.rss",
"http://www.cert.org/channels/certcc.rdf",
"http://www.eff.org/news/eff_news.rss",
"http://www.emailsecurity.co.uk/intergration/mnn.rss",
"http://www.fool.com/xml/foolnews_rss091.xml",
"http://www.freedom-to-tinker.com/index.rdf",
"http://www.heise.de/newsticker/heise.rdf",
"http://www.heise.de/tp/news.rdf",
"http://www.hideaway.net/home/public_html/backend/hideaway.rdf",
"http://www.hk94.com/weblog/b2rss.xml",
"http://www.infoanarchy.org/backend.rdf",
"http://www.jerf.org/irights/categories/jabber/rss.xml",
"http://www.joelonsoftware.com/rss.xml",
"http://www.kill-hup.com/killhupcom.rdf",
"http://www.krit.de/rss.xml",
"http://www.kuro5hin.org/backend.rdf",
"http://www.linuxsecurity.com/linuxsecurity_advisories.rdf",
"http://www.linuxsecurity.com/linuxsecurity_articles.rdf",
"http://www.machinelake.com/index.rdf",
"http://www.macintoshsecurity.com/backend.php",
"http://www.miladus.org/mt/index.rdf",
"http://www.moreover.com/cgi-local/page?index_computersecurity+rss",
"http://www.mozilla.org/newsbot/newsbot.rdf",
"http://www.net-security.org/dl/bck/advi.rss",
"http://www.net-security.org/dl/bck/news.rss",
"http://www.net-security.org/dl/bck/press.rss",
"http://www.net-security.org/dl/bck/soli.rss",
"http://www.net-security.org/dl/bck/sowi.rss",
"http://www.net-security.org/dl/bck/vuln.rss",
"http://www.netsys.com/news.rdf",
"http://www.newsisfree.com/HPE/xml/feeds.dir/76/1676.xml",
"http://www.newsisfree.com/HPE/xml/feeds/22/3722.xml",
"http://www.newsisfree.com/HPE/xml/feeds/27/827.xml",
"http://www.newsisfree.com/HPE/xml/feeds/39/1439.xml",
"http://www.newsisfree.com/HPE/xml/feeds/56/3156.xml",
"http://www.newsisfree.com/HPE/xml/feeds/61/961.xml",
"http://www.newsisfree.com/HPE/xml/feeds/69/3369.xml",
"http://www.newsisfree.com/HPE/xml/feeds/72/1372.xml",
"http://www.newsisfree.com/HPE/xml/feeds/75/3875.xml",
"http://www.newsisfree.com/HPE/xml/feeds/85/3785.xml",
"http://www.newsisfree.com/HPE/xml/feeds/93/1393.xml",
"http://www.newsisfree.com/HPE/xml/feeds/newscat51.xml",
"http://www.newsisfree.com/HPE/xml/newchannels.xml",
"http://www.newsisfree.com/rss/01113b98faf26526b26b7d38e029b048/",
"http://www.newsisfree.com/rss/04aaf6789af224d459ad31d6b0d5caf3/",
"http://www.newsisfree.com/rss/07736817812e567014b33a183e66ae53/",
"http://www.newsisfree.com/rss/10d24d0c7164512b02283cb4425b0c73/",
"http://www.newsisfree.com/rss/1819911d30050bcd7ed3a79d02148a14/",
"http://www.newsisfree.com/rss/248e1dd96ba1931378c5740151868f9c/",
"http://www.newsisfree.com/rss/3065dc800bd518d51e2912d4f8b811d1/",
"http://www.newsisfree.com/rss/37ec18533313bf6bcf88e6d4d78adca5/",
"http://www.newsisfree.com/rss/3eb46a687428d4baa7c60d1964f1684f/",
"http://www.newsisfree.com/rss/4754dc96d69a4add6b4cc1976750c1b5/",
"http://www.newsisfree.com/rss/51a5582712dd2e73cb558925b06cfa94/",
"http://www.newsisfree.com/rss/52df6adc2105c59c2939a6bc5b456e61/",
"http://www.newsisfree.com/rss/60425ebaffc7cb6c5e746ed8c9181178/",
"http://www.newsisfree.com/rss/62518046d78833a7252785f9d83f4c5e/",
"http://www.newsisfree.com/rss/6d6324de5e8a7bbfc3e448de53184df4/",
"http://www.newsisfree.com/rss/753e8266a395ac45828af9c018478c6b/",
"http://www.newsisfree.com/rss/7d80dc7137489a4e1c42780ec312a35c/",
"http://www.newsisfree.com/rss/8a089250f0e79cefa9fb6531ef8cb701/",
"http://www.newsisfree.com/rss/8ec0f81e7a0b419581102feb8cc20770/",
"http://www.newsisfree.com/rss/990b9e79153b912def869b45c1669cbc/",
"http://www.newsisfree.com/rss/9ce545cafd18c33faf8f68319b9ab51e/",
"http://www.newsisfree.com/rss/a9ab436ab9292c05286cb55567be92b1/",
"http://www.newsisfree.com/rss/aa6a8905234aa3b7b743217b0620302a/",
"http://www.newsisfree.com/rss/aced7a34e6cc8e229e3fd7f17871caf8/",
"http://www.newsisfree.com/rss/ae2a87d79159e943c7470e10bdd93eff/",
"http://www.newsisfree.com/rss/b2f31d4de7994f4b8adcdb1cfa518472/",
"http://www.newsisfree.com/rss/b3944a268657aaec3ed7daaefbae91c3/",
"http://www.newsisfree.com/rss/be13c124e40a79c256c0e2fb9d2917bf/",
"http://www.newsisfree.com/rss/c97f1fa6bf432dd1063c77ba5fe6298c/",
"http://www.newsisfree.com/rss/c9d219cfb60e9b7dfac09683c1cd5b74/",
"http://www.newsisfree.com/rss/d44e9d3fc48cc5dcda141c1d4d2df3ce/",
"http://www.newsisfree.com/rss/dbbe2af6525fdd5a81adf9d523ac9f82/",
"http://www.newsisfree.com/rss/e0f7b221b94992f1afdb42e938f84d68/",
"http://www.newsisfree.com/rss/e2be46fb7a567253c2ac3e453d7bcaaa/",
"http://www.newsisfree.com/rss/ec1bb2b0e1810978abb78364ff873809/",
"http://www.newsisfree.com/rss/f2998ed4f8ef02160776d20deb75aaa4/",
"http://www.newsisfree.com/rss/f34e103eafbf56291c2529f1c8ddb635/",
"http://www.newsisfree.com/rss/f80ba9695c09a0b856ca8f18ff28e3a2/",
"http://www.orbtech.com/blog/pobrien/index.rdf",
"http://www.oreillynet.com/~rael/lang/python/peerkat/index.rss",
"http://www.ourfavoritesongs.com/users/adam@curry.com/rss/curryCom.xml",
"http://www.ozzie.net/blog/rss.xml",
"http://www.peek-a-booty.org/pbhtml/backend.php",
"http://www.python.org/channews.rdf",
"http://www.pythonware.com/news.xml",
"http://www.randomhacks.net/backend/rss.xml",
"http://www.rklau.com/tins/rss.xml",
"http://www.roell.net/weblog/Blogfeed.pl",
"http://www.schockwellenreiter.de/rss.xml",
"http://www.schoolblogs.com/harrypotter/xml/rss.xml",
"http://www.security-protocols.com/backend.php",
"http://www.sophos.com/virusinfo/infofeed/topten.xml",
"http://www.state.wv.us/wvsca/Clerk/Topics/Criminal/rss.xml",
"http://www.talkleft.com//index.rdf",
"http://www.textlab.de/itw/itw.xml",
"http://www.tidbits.com/channels/tidbits.rss",
"http://www.virtualchase.com/rssfeeds/tvc_rss.xml",
"http://www.whostolethetarts.com/index.rdf",
"http://www.wired.com/news_drop/netcenter/netcenter.rdf",
"http://www.xmlhack.com/rss10.php?cat=18",
"http://www.yaywastaken.com/amazon/amazon-rss.asp?keywords=computercrime",
"http://www.yaywastaken.com/amazon/amazon-rss.asp?keywords=cybercrime",
"http://www.yaywastaken.com/amazon/amazon-rss.asp?keywords=cyberlaw",
"http://www.yaywastaken.com/amazon/amazon-rss.asp?keywords=cyberterror",
"http://www.yaywastaken.com/amazon/amazon-rss.asp?keywords=cyberwar",
"http://www.zoyth.com/amazonblog/rss.php",
"http://x42.com/rss/rfc.rss",
#"http://blogdex.media.mit.edu/xml/fresh.asp?c=25",
#"http://freshmeat.net/backend/fm.rdf",
#"http://goodshit.phlap.net/index.xml",
#"http://wmf.editthispage.com/xml/scriptingNews2.xml",
"http://jrobb.userland.com/rss.xml",
"http://kairosnews.org/backend.php",
"http://kode-fu.com/geek/rss.xml",
#"http://koeln.ccc.de/backend/links.rdf.php",
"http://koeln.ccc.de/backend/headlines.rdf.php",
"http://krit.de/kritlog/rss.xml",
"http://kt.zork.net/GNUe/rss.rdf",
"http://kt.zork.net/kde/rss.rdf",
"http://kt.zork.net/kernel-traffic/rss.rdf",
"http://kt.zork.net/wine/rss.rdf",
"http://lambda.weblogs.com/xml/rss.xml",
"http://lastminute.rotorjet.com/xml/rss.xml",
"http://lessig.org/index.rdf",
"http://live.curry.com/rss.xml",
"http://monkeyfist.com/rss1.php3",
"http://online.effbot.org/rss.xml",
#"http://radio.weblogs.com/0112292/rss.xml",
"http://rss.actsofvolition.com",
#"http://slashdot.org/apple.rss",
#"http://slashdot.org/bsd.rss",
#"http://slashdot.org/interviews.rss",
"http://trainedmonkey.com/news/rss.php?s=6",
"http://weblog.infoworld.com/udell/rss.xml",
"http://www.aaronsw.com/weblog/index.xml",
"http://www.bbc.co.uk/syndication/feeds/news/ukfs_news/front_page/rss091.xml",
"http://www.example.com/rss.xml",
#"http://www.freshmeat.net/backend/fm-releases.rdf",
"http://www.krit.de/kritlog/rss.xml",
"http://www.macnn.com/macnn.rdf",
"http://www.newsisfree.com/HPE/xml/feeds/15/2315.xml",
"http://www.newsisfree.com/HPE/xml/feeds/43/2843.xml",
"http://www.rklau.com/tins/rss.xml",
"http://www.scripting.com/rss.xml",
"http://www.tarasue4u.com/xml/rss.xml",
"http://www.theregister.co.uk/tonys/slashdot.rdf",
"http://www.voidstar.com/rssify.php?url=http://bgbg.blogspot.com",
"http://www.voidstar.com/rssify.php?url=http://excitedutterances.blogspot.com/",
"http://zem.squidly.org/weblog/rss.xml",
# "http://www.syndic8.com/genfeed.php?Format=rss",
    ]


# inspired by the effbot
charref_re = re.compile('&#([0-9]+);')
charrefhex_re = re.compile('&#x([0-9a-fA-F]+);')
entity_re = re.compile("&(\w+?);")

def descape_entity(m, defs=htmlentitydefs.entitydefs):
    # callback: translate one entity to its ISO Latin value
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0) # use as is

def descape_charref(m):
    try:
        return chr(int(m.group(1)))
    except ValueError:
        return "&#%s;" % m.group(1)

def descape_charrefhex(m):
    return chr(int(m.group(1), 16))
    
def descape(string):
    string = entity_re.sub(descape_entity, string)
    string = charrefhex_re.sub(descape_charrefhex, string)
    return charref_re.sub(descape_charref, string)

def fixItem(item, sourceurl, channel = {}):
    # add guid if needed
    if 'guid' not in item:
        item['guid'] = "%s-%s" % (channel.get("link", channel.get("description", "unspec")), md5.new("%s%s%s" % (item.get("title", ""), item.get("link", ""), item.get("description", ""))).hexdigest()) 
    if "date" in item:
        item["TVdateobject"] = mx.DateTime.Parser.DateTimeFromString(item["date"])
    else:
        item["TVdateobject"] = mx.DateTime.now()
    item["TVsourceurl"] = sourceurl
    if "title" in item:
        item["title"] = descape(item["title"])
    if "description" in item:
        item["description"] = descape(item["description"])
        

def fixService(service = {}, etag = None, modified = None):
    service["TVetag"] = etag
    service["TVmodified"] = modified
    service["TVlastfetched"] = mx.DateTime.now()
    if "TVcreated" not in service:
        service["TVcreated"] = mx.DateTime.now()
    return service

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        urls = sys.argv[1:]
    else:
        urls = URLS
    from pprint import pprint

    urls = tv.aggregator.db.services.getsubscriptions()
    random.shuffle(urls)

    for url in urls:
        print url
        service = tv.aggregator.db.services.getfeedinfo(url)
        result = rssparser.parse(url)
        service.update(result["channel"])
        fixService(service, result.get("etag"), result.get("modified"))
        print "->", 
        sys.stdout.flush()
        for x in result["items"]:
            fixItem(x, url, result["channel"])
            if tv.aggregator.db.items.checkdupe(x):
                print "-",
                sys.stdout.flush()
            else:
                service["TVitemsfetched"] = service.get("TVitemsfetched", 0) + 1
                service["TVlastnewitem"] = mx.DateTime.now() 
                try:
                    tv.aggregator.db.items.saveitem(x)
                except:
                    print "DUPERROR",
                print "*",
            #pprint(x)
        print
        #pprint(service)
        tv.aggregator.db.services.savefeedinfo(service)
        
    tv.aggregator.db.items.save()
    #tv.aggregator.db.items.getitemsByDate("2002-10-22 12:53:27.15", 2)
