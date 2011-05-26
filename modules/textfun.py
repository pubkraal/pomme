# vim: set fileencoding=utf-8 :
import random

def pubmsg(connection, event):
    message = event._arguments[0].strip()
    command = message.split()[0]
    words = ' '.join(message.split()[1:])
    if command == '!reverse':
        connection.privmsg(event.target(), words[::-1])
    elif command == '!breezah':
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

    # Bot love specifics down here.
    elif message.lower() == 'hello!':
        nickname = event.source().split('!')[0]
        if nickname.lower() == 'blabber':
            connection.privmsg(event.target(), "Hi %s!" % (nickname,))
