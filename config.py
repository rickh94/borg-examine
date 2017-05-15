#!/usr/bin/env python3
# read configuration file for borg-examine program
import os, configparser, sys, subprocess

def parseconfig():
    config = configparser.ConfigParser()
    home = os.path.expanduser("~")
    config_path = home + '/.config/borg-examine/borg-examine.conf'

    # check for configuration file and create one if it does not.
    if not os.path.isfile(config_path):
        print("No configuration file found. Let's create one now.")

        config['Repo'] = {}
        config['Recovery'] = {}
        config['System'] = {}

        config['Repo']['Path'] = input("Please enter the full path to your borg repository.\n")
        config['Repo']['Passphrase'] = input("Please enter your borg repo passphrase.\n")

        default_mnt_path = home + '/recover_mount'
        yn = input("The default path for mounting backups is: {}. Is this ok?[yn] ".format(default_mnt_path)).lower()
        while True:
            try:
                if yn[0] == 'n':
                    config['Recovery']['Mountpoint'] = input("Please enter the mountpoint you would like to use.\n")
                    break
                elif yn[0] == 'y':
                    config['Recovery']['Mountpoint'] = default_mnt_path
                    break
                else:
                    yn = input("Please enter [y]es or [n]o. ").lower()
            except IndexError:
                yn = input("Please enter [y]es or [n]o. ").lower()


        default_extract_path = home + '/recovered_files'
        yn = input("The default path for mounting backups is: {}. Is this ".format(default_extract_path) +
                "ok?[yn] ").lower()
        while True:
            try:
                if yn[0] == 'n':
                    config['Recovery']['Extractpoint'] = input("Please enter the folder you would like to use.\n")
                    break
                elif yn[0] == 'y':
                    config['Recovery']['Extractpoint'] = default_extract_path
                    break
                else:
                    yn = input("Please enter [y]es or [n]o. ").lower()
            except IndexError:
                yn = input("Please enter [y]es or [n]o. ").lower()

        config['System']['OpenCommand'] = input("Please enter a shell command for opening files and folders.\n")
        try:
            if not os.path.exists(home + '/.config/borg-examine'): os.makedirs(home + '/.config/borg-examine')
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            print("Your configuration file has been written. It can be edited at any time at {}"\
                    .format(config_path))
        except PermissionError:
            print("Cannot write to {}. Please change ownership/permissions and try again.".format(config_path))
            sys.exit()

    # read configuration file
    config.read(config_path)


    options = {'repopath': config['Repo']['Path'],
            'passphrase': config['Repo']['passphrase'],
            'mountpoint': config['Recovery']['mountpoint'],
            'opencommand': config['System']['opencommand']
            }

    return options

