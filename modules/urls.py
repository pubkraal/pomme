import re
import urllib2
import time
import traceback

import lxml.html

URLCACHE = []


def pubmsg(connection, event):
    global URLCACHE
    message = event._arguments[0].strip()
    command = message.split()[0].lower()

    urlpattern = 'http(s)?://([^\s])+'
    urlmatch = re.search(urlpattern, message)

    if urlmatch:
        try:
            if urlmatch.group() not in URLCACHE:
                URLCACHE = URLCACHE[-4:]
                URLCACHE.append(urlmatch.group())
                title = get_title_from_URL(urlmatch.group())
                if title:
                    connection.privmsg(event.target(), "title: %s" % (title,))
        except Exception as e:
            traceback.print_exc()

    if command == '!urls':
        for url in URLCACHE[:5]:
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

