def pubmsg(connection, event):
    msg = event._arguments[0].strip()
    if msg[:3].lower() == 'pom':
        connection.privmsg(event.target(), "pom")
