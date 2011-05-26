import cookie
import control
import paradise
import pom
import urls
import textfun
import traceback
import log

import sys

all = ['cookie', 'urls', 'pom', 'paradise', 'control', 'textfun', 'log']

hooks = {'privmsg': [], 'pubmsg': [], 'cycle': []}

hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)
hooks['pubmsg'].append(textfun)
hooks['pubmsg'].append(log)
hooks['pubmsg'].append(paradise)

hooks['privmsg'].append(control)

for modname in sys.modules:
    if modname[:8] != 'modules.' or not modname.split('.')[1] in all:
        continue
    try:
       sys.modules[modname] = reload(sys.modules[modname])
    except:
        traceback.print_exc()

