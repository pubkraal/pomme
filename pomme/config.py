import os
from ConfigParser import ConfigParser


class Config(object):
    def __init__(self, extra):
        self.cfg = ConfigParser()
        files = ['/etc/pomme.conf', os.path.expanduser("~/.pomme")]
        if extra:
            files.append(extra)
        self.cfg.read(files)

        self.servers = []

        for section in self.cfg.sections():
            if section[:6] == "server":
                items = dict(self.cfg.items(section))
                s = ServerConfig(items.get('host'),
                        [items.get('nick'), items.get('nick2')],
                        items.get('port', 6667),
                        items.get('ssl', False),
                        items.get('password', ''),
                        items.get('channels', '').split(','))
                self.servers.append(s)

    def get_servers(self):
        return self.servers

    def get(self, section, name, default=None):
        return getattr(self.cfg, name, default)


class ServerConfig(object):
    def __init__(self, hostname, nicknames, port=6667, ssl=False,
                password=None, channels=[]):
        self.hostname = hostname
        self.port = port
        self.nicknames = nicknames
        self.ssl = ssl
        self.password = password
        self.channels = channels
