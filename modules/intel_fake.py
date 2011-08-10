def pubmsg(connection, event):
    message = event._arguments[0].strip()
    cmd = message.split()[0]
    if cmd == '!intel':
        connection.privmsg(event.target(), "pomme is currently not gathering intel. intel_fake.py")

def privmsg(connection, event):
    pass
