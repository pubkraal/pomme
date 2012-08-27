#!/usr/bin/env python
import argparse
import modules
from pomme import pomme, config


def je_suis_une_pomme():
    parser = argparse.ArgumentParser(description='pomme irc bot')
    parser.add_argument('-c', '--config', dest="extraconfig", default="",
        help="Supply an extra configuration file for parsing options from.")

    args = parser.parse_args()

    cfg = config.Config(args.extraconfig)

    bot = pomme.Pomme(cfg, modules)

    try:
        bot.run()
    except KeyboardInterrupt:
        print "Caught interrupt"
        bot.close()
    print "Exit"


if __name__ == "__main__":
    je_suis_une_pomme()
