def pubmsg(connection, event):
    msg = event._arguments[0].strip()
    if msg.lower() == 'pom':
        connection.privmsg(event.target(), "pom")
