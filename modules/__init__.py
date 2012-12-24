import butt
import convert
import paradise
import pom
import urls
import textfun
import traceback
import log
import questions

import sys

all = ['butt', 'cookie', 'urls', 'pom', 'paradise', 'control', 'textfun',
       'log', 'convert', 'questions']

hooks = {'privmsg': [], 'pubmsg': [], 'cycle': []}

hooks['pubmsg'].append(butt)
hooks['pubmsg'].append(convert)
hooks['pubmsg'].append(urls)
hooks['pubmsg'].append(pom)
hooks['pubmsg'].append(textfun)
hooks['pubmsg'].append(log)
hooks['pubmsg'].append(paradise)
hooks['pubmsg'].append(questions)

hooks['privmsg'].append(log)

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
        print "Reloading", modname
        sys.modules[modname] = reload(sys.modules[modname])
    except:
        traceback.print_exc()
