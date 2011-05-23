import irclib


class Pomme(object):
    def __init__(self, configuration, modules):
        self.config = configuration
        self.mods = modules
        self.irc = irclib.IRC()
        self.servers = []
        self.terminate = False

    def run(self):
        for server in self.config.get_servers():
            try:
                s = self.irc.server()
                s.join_channels = server.channels
                c = s.connect(server.hostname, server.port,
                        server.nicknames[0], ssl=server.ssl,
                        password=server.password)
                c.add_global_handler("privmsg", self.handle_privmsg)
                c.add_global_handler("pubmsg", self.handle_pubmsg)
                c.add_global_handler("umode", self.handle_umode)

                self.servers.append(s)

            except Exception as e:
                print e
                raise e

        while not self.terminate:
            self.irc.process_once(0.2)

        self.close()

    def close(self):
        for server in self.servers:
            if server.is_connected():
                server.disconnect("Doei!")

    def reload(self):
        try:
            print "Reloading modules"
            self.mods = reload(self.mods)
        except Exception as e:
            print "Couldn't reload modules:", e

    def connect(self, hostname, port, nickname):
        return self.connection.connect(hostname, port, nickname)

    def handle_privmsg(self, connection, event):
        msg = event._arguments[0].lower()
        if msg == "vertrek, nu":
            self.terminate = True
        elif msg == "rehash":
            self.reload()
        elif msg[:4] == "join":
            connection.join(msg[5:])

    def handle_pubmsg(self, connection, event):
        for x in self.mods.hooks.get('pubmsg'):
            try:
                x.pubmsg(connection, event)
            except Exception as e:
                print "OHGOD :psyduck:,", e

    def handle_umode(self, connection, event):
        if event.arguments()[0] == "+i":
            for channel in connection.join_channels:
                print "Joining", channel
                connection.join(channel)
