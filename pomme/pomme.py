import irclib


class Pomme(object):
    def __init__(self, configuration, modules):
        self.config = configuration
        self.mods = modules
        self.irc = irclib.IRC()
        self.servers = []
        self.terminate = False

    def run(self):
        self.irc.add_global_handler("privmsg", self.handle_privmsg)
        self.irc.add_global_handler("pubmsg", self.handle_pubmsg)
        self.irc.add_global_handler("umode", self.handle_umode)
        for server in self.config.get_servers():
            try:
                s = self.irc.server()
                s.join_channels = server.channels
                c = s.connect(server.hostname, server.port,
                        server.nicknames[0], ssl=server.ssl,
                        password=server.password)

                print "Connection:", c

                self.servers.append(s)

                for channel in server.channels:
                    try:
                        s.join(channel)
                    except Exception as e:
                        print e

            except Exception as e:
                print e
                raise e

        while not self.terminate:
            self.irc.process_once(0.2)
            for x in self.mods.hooks.get('cycle', []):
                try:
                    x.cycle(self.servers)
                except Exception as e:
                    print "OHGOD :psyduck:, iets fout in de cycle!"

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

        for x in self.mods.hooks.get('privmsg'):
            try:
                x.privmsg(connection, event)
            except Exception as e:
                print "OHGOD :psyduck,", e

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
