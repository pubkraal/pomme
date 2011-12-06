import io
import os
import re
import urllib2
import time
import traceback
try:
    import cPickle as pickle
except:
    import pickle

import lxml.html

PICKLEFILE = os.path.expanduser("~/.pommeurls")
try:
    URLCACHE = pickle.load(io.open(PICKLEFILE, 'r+b'))
except:
    URLCACHE = {}


def pubmsg(connection, event):
    global URLCACHE
    message = event._arguments[0].strip()
    command = message.split()[0].lower()

    uid = '/'.join([connection.server, event.target()])
    if not uid in URLCACHE:
        URLCACHE[uid] = []

    urlpattern = 'http(s)?://([^\s])+'
    urlmatch = re.search(urlpattern, message)

    if urlmatch:
        try:
            if urlmatch.group() not in URLCACHE:
                URLCACHE[uid] = URLCACHE[uid][-50:]
                URLCACHE[uid].append(urlmatch.group())
                pickle.dump(URLCACHE, io.open(PICKLEFILE, 'w+b'))
                title = get_title_from_URL(urlmatch.group())
                if title:
                    connection.privmsg(event.target(), "title: %s" % (title,))
        except Exception as e:
            traceback.print_exc()

    if command == '!urls':
        dat = message.split()
        num = 5
        try:
            num = min(10, abs(int(dat[1])))
        except: pass
        for url in URLCACHE[uid][-num:]:
            connection.privmsg(event.target(), url)
            time.sleep(0.5)


def get_title_from_URL(url):
    retval = ''
    doc = lxml.html.parse(url)

    try:
        retval = doc.find('.//title').text
        retval = re.sub('\s+', ' ', retval).strip()
    except Exception as e:
        traceback.print_exc()

    return retval
