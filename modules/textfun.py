# vim: set fileencoding=utf-8 :
import random

store_ = {}

def pubmsg(connection, event):
    global store_
    message = event._arguments[0].strip()
    command = message.split()[0]
    words = ' '.join(message.split()[1:])

    msgkey = ';'.join([connection.server, event.target()])

    if command == '!reverse':
        if words == '_':
            connection.privmsg(event.target(), store_[msgkey][::-1])
        else:
            connection.privmsg(event.target(), words[::-1])
    elif command == '!breezah':
        if words == '_':
            words = store_[msgkey]
        nwords = ''
        for idx, letter in enumerate(words):
            nwords += letter.upper() if not idx % 2 else letter.lower()
        connection.privmsg(event.target(), nwords)

    elif message.lower() == 'hallo pomme':
        user = event.source().split('!')[0]
        connection.privmsg(event.target(), "Hai! <3")

    elif 'vakansie' in message.lower():
        connection.privmsg(event.target(), 'Ik kan ook wel verkansie '
            'gebruiken naah!')

    elif message.lower() == 'chicken?':
        connection.privmsg(event.target(),
            "http://isotropic.org/papers/chicken.pdf")

    elif 'spaans' in message.lower():
        connection.privmsg(event.target(),
            random.choice(['El pollo diablo!', 'Yo no hablo Español!']))

    elif 'dronten' in message.lower():
        connection.privmsg(event.target(), "Flevoland :'D")

    # Bot love specifics down here.
    elif message.lower() == 'hello!':
        nickname = event.source().split('!')[0]
        if nickname.lower() == 'blabber':
            connection.privmsg(event.target(), "Hi %s!" % (nickname,))

    elif 'blabber' in message.lower():
        connection.privmsg(event.target(), 'blabberuuu~~ <3~')

    else:
        store_[msgkey] = message
