import datetime
import io
import os
from lxml import etree
try:
    import cPickle as pickle    # NOQA
except:
    import pickle # NOQA

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
        self.title = node.find("//title").text
        self.link = node.find("//link").text
        self.guid = node.find("//guid").text
        self.link = node.find("//link").text
        self.description = node.find("//description").text
        self.pubdate = node.find("//pubdate").text


class RSSFeed(object):
    def __init__(self, feed):
        self.feed = feed
        self.items = []

    def update(self):
        self.items = []

        doc = etree.parse(self.feed)
        items = doc.findall('//items')
        for item in items:
            self.items.append(RSSItem(item))


def pubmsg(connection, event):
    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    (command, remainer) = message.split(" ", 1)

    if command in ('!feeds', '!rss-feeds'):
        connection.privmsg(event.target(),
                           'Ik ken momenteel geen rss feeds, voor dit kanaal')


def privmsg(connection, event):
    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    (command, remainder) = message.split(" ", 1)

    if command in ('!add-feed',):
        (feed, channels) = remainder.split(1)
        try:
            add_feed(connection, event.target(), feed, channels.split())
        except RSSException:
            return
        except Exception as e:
            print "Exception during adding RSS feed:", e


def cycle(connections):
    now = datetime.datetime.now()
    feeds = get_feeds_to_check(now)
    for feed in feeds:
        FEEDCACHE[feed]['lastchecked'] = now
        feed.update()

        if feed.has_new(now):
            spam(feed.items[0], FEEDCACHE[feed], connections)


def spam(feed, feeddata, connections):
    print feed
    print feeddata
    print connections


# Supporting functions
def get_feeds_to_check(now):
    global FEEDCACHE
    global CHECK_INTERVAL

    to_check = []

    check_time = datetime.timedelta(seconds=CHECK_INTERVAL)
    for feed, data in FEEDCACHE.iteritems():
        if data['last_checked'] + check_time < now:
            to_check.append(feed)

    return to_check


def add_feed(connection, target, feed, channels):
    if not feed in FEEDCACHE:
        if not check_feed(feed):
            raise RSSException("Not a RSS feed")
        add_feed_to_cache(feed)
    add_channels_to_feed([gen_uid(connection.server, channel)
                          for channel
                          in channels])
    connection.privmsg(target, u"added.")


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
