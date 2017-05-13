#!/usr/bin/env python3
# read configuration file for borg-examine program
import os, configparser

config = configparser.ConfigParser()
home = os.path.expanduser("~")
config_path = home + '/.config/borg-examine/borg-examine.conf'

# check for configuration file and create one if it does not.
if not os.path.isfile(config_path):
    print("No configuration file found. Let's create one now.")

# read configuration file
config.read(config_path)

# Assign fields to global variables
borg_path = config['Borg']['BorgPath']
repo_path = config['Repo']['RepoPath']
passphrase = config['Repo']['Passphrase']
mountpoint = config['Mount']['mountpoint']
# print('borg_path: {}, repo_path: {}, passphrase: {}, mountpoint: {}'\
#         .format(borg_path, repo_path, passphrase, mountpoint))
