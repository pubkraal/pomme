def pubmsg(connection, event):
    message = event._arguments[0].strip()
    command = message.split()[0]
    words = ' '.join(message.split()[1:])
    if command == '!reverse':
        connection.privmsg(event.target(), words[::-1])
    elif command == '!breezah':
        nwords = ''
        for idx, letter in enumerate(words):
            nwords += letter.upper() if not idx % 2 else letter.lower()
        connection.privmsg(event.target(), nwords)
