import io
import os
import re
import time
import traceback
import json

import lxml.html

URLFILE = os.path.expanduser("~/.pommeurls")
try:
    URLCACHE = json.load(io.open(URLFILE, 'r+b'))
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
                json.dump(URLCACHE, io.open(URLFILE, 'w+b'))
                title = get_title_from_URL(urlmatch.group())
                if title:
                    connection.privmsg(event.target(), "title: %s" % (title,))
        except Exception:
            traceback.print_exc()

    if command == '!urls':
        dat = message.split()
        num = 5
        try:
            num_ = abs(int(dat[1])) or 5
            num = min(5, num_)
        except:
            pass
        for url in URLCACHE[uid][-num:]:
            connection.privmsg(event.target(), url)
            time.sleep(0.5)


def get_title_from_URL(url):
    retval = ''
    doc = lxml.html.parse(url)

    try:
        retval = doc.find('.//title').text
        retval = re.sub('\s+', ' ', retval).strip()
    except Exception:
        traceback.print_exc()

    return retval
