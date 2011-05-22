from . import cookie
from . import control
from . import pom
from . import urls
from . import textfun
from . import log

all = ['cookie', 'urls', 'pom', 'control', 'textfun', 'lol']

hooks = {'privmsg': [], 'pubmsg': []}

hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)
hooks['pubmsg'].append(textfun)
hooks['pubmsg'].append(log)

hooks['privmsg'].append(control)

