import random

ANSWERS = ('Google het maar.',
           'Weet ik veel.',
           'M\'n 8-ball zegt "val dood".',
           'Leuk he, dingen vragen aan botjes?',
           'Wees eerlijk, wat verwacht je nu precies?')

NUMBERS = tuple(range(100) + [127, 1337])

def pubmsg(connection, event):
    message = event._arguments[0].strip()
    target = event.target()
    s = connection

    if (message.startswith("pomme, ") or message.startswith("pomme: ")) and \
        message[-1] == '?':
        if message.split()[1] == 'hoeveel':
            s.privmsg(target, '%s%d' % (random.choice(('ongeveer ', '')),
                                        random.choice(NUMBERS)))
        else:
            s.privmsg(target, random.choice(ANSWERS))
