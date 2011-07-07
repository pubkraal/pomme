def pubmsg(connection, event):
    message = event._arguments[0].strip()
    command = message.split()[0]
    if command == "convert":
        data = message.split()

        if data[1:4] == ["hex", "to", "rgb"] and data[4]:
            hexval = int(data[4].replace("#", ""), 16)
            print hexval, data[4]
            r = (hexval & 0xFF0000) >> 16
            g = (hexval & 0x00FF00) >> 8
            b = (hexval & 0x0000FF)

            connection.privmsg(event.target(), "%s is %d, %d, %d" % (data[4],
                                                                     r, g, b))
