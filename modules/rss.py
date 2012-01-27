import sqlite3


def pubmsg(connection, event):
    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    command = message.split()[0]
    words = ' '.join(message.split()[1:])

    if command in ('!feeds', '!rss-feeds'):
        connection.privmsg(event.target(),
                           'Ik ken momenteel geen rss feeds, voor dit kanaal')


def privmsg(connection, event):
    message = event._arguments[0].strip()
    if message[0] != '!':
        return
    command = message.split()[0]
    words = ' '.join(message.split()[1:])

    if command in ('!add-feed',):
        print ">> Add feed not yet implemented"
    elif command in ('!feeds',):
        connection.privmsg(event.target(), 'Yo, ik ken nog geen feeds')


def cycle(connections):
    pass
