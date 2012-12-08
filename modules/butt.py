import random
from buttes import buttifier


def pubmsg(connection, event):
    message = event._arguments[0].strip()
    num = random.randrange(0, 100)
    print "Buttes:", num
    if num < 5:
        connection.privmsg(event.target(), buttifier.buttify(message))
