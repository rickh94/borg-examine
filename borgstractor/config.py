#!/usr/bin/env python3
# read configuration file for borg-examine program
import os, configparser, sys, subprocess
from borgstractor import settings

def parseconfig():
    config = configparser.ConfigParser()
    home = os.path.expanduser("~")
    config_folder = home + '/.config/borgstractor/'
    config_path = config_folder + 'borgstractor.conf'

    # check for configuration file and create one if it does not.
    if not os.path.isfile(config_path):
        print("No configuration file found. Let's create one now.")
        make_config_file(home, config, config_folder, config_path)
    # end if

    # read configuration file
    config.read(config_path)

    options = {'repopath': config['Repo']['Path'],
            'passphrase': config['Repo']['passphrase'],
            'mountpoint': config['Recovery']['mountpoint'],
            'opencommand': config['System']['opencommand'],
            'extractdir': config['Recovery']['extractdir']
            }
    for name, val in options.items():
        setattr(settings, name, val)


# creates configuration file if none present
def make_config_file(home, config, config_folder, config_path):
    # create sections
    config['Repo'] = {}
    config['Recovery'] = {}
    config['System'] = {}

    # get input from user
    config['Repo']['Path'] = input("Please enter the full path to your borg repository.\n")
    config['Repo']['Passphrase'] = input("Please enter your borg repo passphrase.\n")

    # offer defaults to user if not available.
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
            # end if
        except IndexError:
            yn = input("Please enter [y]es or [n]o. ").lower()
        # end try
    # end while (user input)


    default_extract_path = home + '/recovered_files'
    yn = input("The default path for recovering files is: {}. Is this ".format(default_extract_path) +
            "ok?[yn] ").lower()
    while True:
        try:
            if yn[0] == 'n':
                config['Recovery']['Extractdir'] = input("Please enter the folder you would like to use.\n")
                break
            elif yn[0] == 'y':
                config['Recovery']['Extractdir'] = default_extract_path
                break
            else:
                yn = input("Please enter [y]es or [n]o. ").lower()
            # end if (user input)
        except IndexError:
            yn = input("Please enter [y]es or [n]o. ").lower()
        # end try
    # end while (user input)

    # shell level command to be run when opening directories.
    config['System']['OpenCommand'] = input("Please enter a shell command for opening files and folders.\n")
    try:
        if not os.path.exists(config_folder): os.makedirs(config_folder)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            print("Your configuration file has been written. It can be edited at any time at {}"\
                .format(config_path))
    except PermissionError:
        print("Cannot write to {}. Please change ownership/permissions and try again.".format(config_path))
        sys.exit()
    # end try
# end def make_config_file
