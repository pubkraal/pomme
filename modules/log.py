def pubmsg(connection, event):
    print "[%s] %r" % (event.target(), event._arguments)
