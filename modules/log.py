def pubmsg(connection, event):
    username = event.source().split('!')[0]
    print "[%s:%s] %r" % (event.target(), username, event._arguments)
