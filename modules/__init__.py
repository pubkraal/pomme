import cookie
import control
import pom
import urls
import textfun
import log

all = ['cookie', 'urls', 'pom', 'control', 'textfun', 'log']

hooks = {'privmsg': [], 'pubmsg': []}

hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)
hooks['pubmsg'].append(textfun)
hooks['pubmsg'].append(log)

hooks['privmsg'].append(control)

for mod in all:
    modname = '.'.join(['modules', mod])
    if modname in sys.modules:
        sys.modules[modname] = reload(sys.modules[modname])

