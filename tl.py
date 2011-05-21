#!/usr/bin/python

import irclib
import sys
import time
import datetime
import urllib2
import re
import BeautifulSoup as bs

irclib.DEBUG = True
irc = irclib.IRC()
server = None
c = None

terminate = False

urls = []


def main():
    global server
    global c
    global terminate
    server = irc.server()
    c = server.connect("xs4all.nl.quakenet.org", 6667, "pomme")
    c.add_global_handler("privmsg", _handle_privmsg)
    c.add_global_handler("pubmsg", _handle_pubmsg)
    c.add_global_handler("umode", _handle_umode)
    while not terminate:
        irc.process_once()
        time.sleep(0.2)
    server.close()


def _handle_privmsg(conn, event):
    print timestamp(), "privmsg", event._arguments
    global terminate
    if event._arguments[0].lower() == "jorik ga weg":
        terminate = True


def _handle_pubmsg(conn, event):
    global server
    global terminate
    global urls
    print timestamp(), "pubmsg", event._arguments, event.target()
    message = event._arguments[0].strip()
    command = message.split()[0]
    urlpattern = 'http(s)?://([^\s])+'
    if message.lower() in ('pom', 'pom!', 'pomme', 'pom?', 'pom.'):
        server.privmsg("#tl.nl", "pom")
    elif command == '!reverse':
        words = ' '.join(message.split()[1:])
        server.privmsg("#tl.nl", words[::-1])
    elif re.search(urlpattern, message):
        try:
            r = re.search(urlpattern, message)
            while len(urls) >= 5:
                urls.pop(0)
            urls.append(r.group())
            title = getTitleFromURL(r.group())
            if title:
                server.privmsg("#tl.nl", "title: %s" % (title,))
        except Exception, e:
            print "iets werkt niet", e
    elif message.lower() == '!urls':
        for url in urls[:5]:
            server.privmsg("#tl.nl", url)


def _handle_umode(conn, event):
    if event.arguments()[0] == '+i':
        server.join("#tl.nl")


def timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def getTitleFromURL(url):
    retval = ''
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    conn = opener.open(url)
    doc = bs.BeautifulSoup(''.join(conn.readlines()))

    retval = doc.fetch('title')[0].string
    retval = re.sub('\s+', ' ', retval)

    return retval

if __name__ == "__main__":
    main()
