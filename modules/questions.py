import random

ANSWERS = ('Google het maar.',
           'Weet ik veel.',
           'M\'n 8-ball zegt "val dood".',
           'Leuk he, dingen vragen aan botjes?',
           'Wees eerlijk, wat verwacht je nu precies?')

def pubmsg(connection, event):
    message = event._arguments[0].strip()
    target = event.target()
    s = connection

    if (message.startswith("pomme, ") or message.startswith("pomme: ")) and \
        message[-1] == '?':
        s.privmsg(target, random.choice(ANSWERS))
