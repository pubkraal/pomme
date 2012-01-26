import datetime

LAST_USED = {}
RATE = 60

def pubmsg(connection, event):
    global LAST_USED
    msg = event._arguments[0].strip()

    if msg.lower() == 'pom':
        uid = '/'.join([connection.server, event.target()])
        if uid not in LAST_USED:
            LAST_USED[uid] = datetime.datetime.now()
        elif not older_than_rate(LAST_USED[uid],
                                 datetime.datetime.now(),
                                 RATE):
            return

        connection.privmsg(event.target(), "pom")

def older_than_rate(t1, t2, rate):
    diff = t2 - t1
    return diff.days > 0 or diff.seconds > rate
