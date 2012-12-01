# vim: set fileencoding=utf-8 :
import random

store_ = {}


def pubmsg(connection, event):
    global store_
    message = event._arguments[0].strip()
    command = message.split()[0]
    words = ' '.join(message.split()[1:])
    msgkey = ';'.join([connection.server, event.target()])

    handler = None

    if command == '!reverse':
        handler = reverse
    elif command == '!breezah':
        handler = breezah
    elif 'vakansie' in message.lower():
        handler = vakansie
    elif 'spaans' in message.lower():
        handler = spaans
    elif 'ugh.pdf' in message.lower():
        handler = unix
    else:
        store_[msgkey] = message

    if handler:
        handler(connection, event, message, command, words, msgkey)


def reverse(connection, event, message, command, words, msgkey):
    if words in ('_', ''):
        connection.privmsg(event.target(), store_[msgkey][::-1])
    else:
        connection.privmsg(event.target(), words[::-1])


def breezah(connection, event, message, command, words, msgkey):
    if words in ('_', ''):
        words = store_[msgkey]
    nwords = ''
    for idx, letter in enumerate(words):
        nwords += letter.upper() if not idx % 2 else letter.lower()
    connection.privmsg(event.target(), nwords)


def vakansie(connection, event, message, command, words, msgkey):
    connection.privmsg(event.target(), 'Ik kan ook wel verkansie '
        'gebruiken naah!')


def spaans(connection, event, message, command, words, msgkey):
    connection.privmsg(event.target(),
        random.choice(['El pollo diablo!', 'Yo no hablo Español!']))


def unix(connection, event, message, command, words, msgkey):
    connection.privmsg(event.target(), "Fuck UNIX.")
