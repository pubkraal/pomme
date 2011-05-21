from . import cookie
from . import control
from . import pom
from . import urls

all = ['cookie', 'urls', 'pom', 'control']

hooks = {'privmsg': [], 'pubmsg': []}

hooks['pubmsg'].append(cookie)
hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)

hooks['privmsg'].append(control)

