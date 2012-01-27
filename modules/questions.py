import random

ANSWERS = ('Google het maar.',
           'Weet ik veel.',
           'M\'n 8-ball zegt "val dood".',
           'Leuk he, dingen vragen aan botjes?',
           'Wees eerlijk, wat verwacht je nu precies?',
           'De sterren zeggen nee.',
           '42.',
           'Zoek het uit',
           'Does a pope shit in the woods?',
           'Because fuck you, that\'s why!',
           'Dat vroeg je vrouw ook vannacht')

NUMBERS = tuple(range(100) + [127, 1337])


def pubmsg(connection, event):
    message = event._arguments[0].strip()
    target = event.target()
    s = connection

    if (message.startswith("pomme, ") or message.startswith("pomme: ")) and \
        message[-1] == '?':
        pieces = message.split()
        if pieces[1] == 'hoeveel':
            s.privmsg(target, '%s%d' % (random.choice(('ongeveer ', '')),
                                        random.choice(NUMBERS)))
        elif len(pieces) == 4 and pieces[2] in ('of', 'or'):
            s.privmsg(target, random.choice((pieces[1], pieces[3][:-1])))
        else:
            s.privmsg(target, random.choice(ANSWERS))
