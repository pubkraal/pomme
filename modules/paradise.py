import lxml.html
import urllib
import traceback

URL = "http://www.radioparadise.com/content.php?name=Playlist"


def pubmsg(connection, event):
    message = event._arguments[0].strip()
    if message.lower() in ['wat horen we nu?', '!np', '!paradise']:
        try:
            doc = lxml.html.fromstring(urllib.urlopen(URL).read())
            last_song = doc.cssselect('tr')[3].getchildren()[1]
            artist = song = None
            for node in last_song.iter():
                artist = node.text or artist
                song = node.tail or song

            if artist and song:
                connection.privmsg(event.target(),
                    'Radio Paradise (.com) speelt nu: %s - %s' % \
                    (artist, song))
        except:
            traceback.print_exc()
