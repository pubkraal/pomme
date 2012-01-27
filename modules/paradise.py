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

    elif message.lower() in ['wat hoorden we net?']:
        try:
            doc = lxml.html.fromstring(urllib.urlopen(URL).read())
            songs = []
            for x in [5, 7, 9]:
                node_ = doc.cssselect('tr')[x].getchildren()[1]
                artist = song = 'n/a'
                for node in node_.iter():
                    artist = node.text or artist
                    song = node.tail or song

                songs.append(dict(artist=artist, song=song))

            if songs:
                for idx, song in enumerate(songs):
                    connection.privmsg(event.target(),
                        '%d: %s - %s' % \
                        (idx + 1,
                         song.get('artist', 'n/a'),
                         song.get('song', 'n/a')))
        except:
            traceback.print_exc()
