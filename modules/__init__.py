import control
import convert
import paradise
import pom
import urls
import textfun
import traceback
import log
import rss
import questions

import sys

all = ['cookie', 'urls', 'pom', 'paradise', 'control', 'textfun', 'log',
       'convert', 'rss', 'questions']

hooks = {'privmsg': [], 'pubmsg': [], 'cycle': []}

hooks['pubmsg'].append(convert)
hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)
hooks['pubmsg'].append(textfun)
hooks['pubmsg'].append(log)
hooks['pubmsg'].append(paradise)
hooks['pubmsg'].append(rss)
hooks['pubmsg'].append(questions)

hooks['privmsg'].append(rss)
hooks['privmsg'].append(log)

hooks['cycle'].append(rss)

try:
    import intel
    all.append('intel')
    hooks['pubmsg'].append(intel)
    hooks['privmsg'].append(intel)
except:
    pass


for modname in sys.modules:
    if modname[:8] != 'modules.' or not modname.split('.')[1] in all:
        continue
    try:
        sys.modules[modname] = reload(sys.modules[modname])
    except:
        traceback.print_exc()
