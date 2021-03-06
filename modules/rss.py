import datetime
import io
import os
import time
import traceback
from lxml import etree
from urlparse import urlparse, ParseResult
try:
    import cPickle as pickle    # NOQA
except:
    import pickle # NOQA

LAST_USED = {}
USE_RATE = 60
PICKLEFILE = os.path.expanduser("~/.pommerss")
CHECK_INTERVAL = 5 * 60
try:
    FEEDCACHE = pickle.load(io.open(PICKLEFILE, 'r+b'))
except:
    FEEDCACHE = {}


class RSSException(Exception):
    pass


class RSSItem(object):
    def __init__(self, node):
        """ Expects an etree-node, so don't try anything else. """
        self.title = node.find("title").text
        self.pubdate = node.find("pubDate").text
        try:
            self.guid = node.find("guid").text
        except:
            # Some feeds don't supply a uid D:
            self.guid = self.pubdate
        try:
            self.link = node.find("link").text
        except:
            # Python.org's rdf doesn't do link tags, but uses guid for this.
            self.link = self.guid
        self.description = node.find("description").text


class RSSFeed(object):
    def __init__(self, feed):
        self.feed = feed
        self.items = []

    def update(self):
        self.items = []

        print "RSS: Pulling", self.feed
        doc = etree.parse(self.feed)
        items = doc.findall('//item')
        for item in items:
            self.items.append(RSSItem(item))


def pubmsg(connection, event):
    global LAST_USED
    global USE_RATE

    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    (command, remainer) = message.split(" ", 1)

    if command in ('!feeds', '!rss-feeds'):
        uid = '/'.join([connection.server, event.target()])

        # Throttling.
        if uid in LAST_USED and not older_than_rate(LAST_USED[uid],
                                 datetime.datetime.now(),
                                 USE_RATE):
            return
        LAST_USED[uid] = datetime.datetime.now()

        feedlist = [feed for feed, data
                         in FEEDCACHE.iteritems()
                         if uid in data['channels']]
        if len(feedlist) > 0:
            connection.privmsg(event.target(), "Lijstje!")
            for feed in feedlist:
                connection.privmsg(event.target(), str(feed))
                time.sleep(1)
        else:
            connection.privmsg(event.target(),
                               'Nope. Go away.')


def privmsg(connection, event):
    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    (command, remainder) = message.split(" ", 1)

    if command in ('!add-feed',):
        (feed, channels) = remainder.split(" ", 1)
        try:
            add_feed(connection,
                     nick_from_source(event.source()),
                     feed,
                     channels.split())
        except RSSException:
            return
        except Exception as e:
            print "Exception during adding RSS feed:", e
    elif command in ('!del-feed',):
        global FEEDCACHE
        if remainder in FEEDCACHE:
            del FEEDCACHE[remainder]
        store_feedcache()


def cycle(connections):
    global FEEDCACHE

    now = datetime.datetime.now()
    feeds = get_feeds_to_check(now)
    if feeds:
        print "Checking", feeds
    for feed in feeds:
        try:
            FEEDCACHE[feed]['lastchecked'] = now

            feed_ = RSSFeed(feed)
            feed_.update()

            if len(feed_.items) == 0:
                continue

            if feed_.items[0].guid > FEEDCACHE[feed]['lastguid']:
                FEEDCACHE[feed]['lastguid'] = feed_.items[0].guid
                spam(feed_.items[0], FEEDCACHE[feed], connections)
        except:
            print "Failed updating", feed
            traceback.print_exc()
    store_feedcache()


def store_feedcache():
    global FEEDCACHE
    global PICKLEFILE
    pickle.dump(FEEDCACHE, io.open(PICKLEFILE, 'w+b'))


def spam(feed, feeddata, connections):
    c_hash = dict([(c.server, c) for c in connections])
    message = '%s - %s' % (feed.title, strip_utm(feed.link))
    for channel in feeddata['channels']:
        server, channel_name = channel.split('/', 1)
        if server in c_hash:
            c = c_hash[server]
            c.privmsg(channel_name, message)


# Supporting functions
def older_than_rate(t1, t2, rate):
    diff = t2 - t1
    return diff.days > 0 or diff.seconds > rate


def get_feeds_to_check(now):
    global FEEDCACHE
    global CHECK_INTERVAL

    to_check = []

    check_time = datetime.timedelta(seconds=CHECK_INTERVAL)
    for feed, data in FEEDCACHE.iteritems():
        if data['lastchecked'] + check_time < now:
            to_check.append(feed)

    return to_check


def add_feed(connection, source, feed, channels):
    connection.privmsg(source, ">>" + str(channels))
    if not channels:
        connection.privmsg(source, "I want channels")
    if not feed in FEEDCACHE:
        if not check_feed(feed):
            raise RSSException("Not a RSS feed")
        add_feed_to_cache(feed)
    add_channels_to_feed([gen_uid(connection.server, channel)
                          for channel
                          in channels], feed)
    store_feedcache()
    connection.privmsg(source, u"added.")


def gen_uid(server, channel):
    return '/'.join([server, channel])


def check_feed(feed):
    try:
        doc = etree.parse(feed)
        return (unicode(doc.getroot().tag) == u'rss')
    except Exception as e:
        print "Exception:", e
        return False


def add_feed_to_cache(feed):
    global FEEDCACHE
    if feed in FEEDCACHE:
        return

    empty_dict = dict()
    empty_dict['lastchecked'] = datetime.datetime(2011, 1, 1)
    empty_dict['lastguid'] = ''
    empty_dict['channels'] = set()

    FEEDCACHE[feed] = empty_dict


def add_channels_to_feed(channels, feed):
    try:
        FEEDCACHE[feed]['channels'].update(channels)
    except Exception as e:
        print e


def nick_from_source(source):
    return source.split('!')[0]


def strip_utm(link):
    """ This method removes utm_* query parts from a link, to make sure our
        privacy is insured. *cough*
    """
    d = urlparse(link)
    query = '&'.join([x for x in d.query.split("&") if x[:4] != 'utm_'])
    return ParseResult(d.scheme,
                       d.netloc,
                       d.path,
                       d.params,
                       query,
                       d.fragment).geturl()
