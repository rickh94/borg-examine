#!/usr/bin/env python3
# read configuration file for borg-examine program
import os, configparser

def parseconfig():
    config = configparser.ConfigParser()
    home = os.path.expanduser("~")
    config_path = home + '/.config/borg-examine/borg-examine.conf'

    # check for configuration file and create one if it does not.
    if not os.path.isfile(config_path):
        print("No configuration file found. Let's create one now.")

    # read configuration file
    config.read(config_path)

    options = {'repopath': config['Repo']['Path'],
                     'passphrase': config['Repo']['passphrase'],
                     'mountpoint': config['Mount']['mountpoint']
                    }
    
    return options

