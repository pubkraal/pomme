#!/usr/bin/python
import argparse
import modules
from pomme import pomme, config


def main():
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
    main()
