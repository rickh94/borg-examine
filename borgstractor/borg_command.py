#!/usr/bin/env python3
# borg_command.py - generates calls to borg programatically instead of
# manually

from borgstractor import config
from borgstractor import settings
import subprocess
import os
import sys
import atexit


# borg_command() - generates borg calls
# mandatory arguments:
#   runtype: either run or popen depending on need
#   subcommand: list, mount, umount, extract
# other arguments:
#   list: (optional) arg[0] can be the name of a specific backup to list files in that backup
#   mount: (mandatory) arg[0] must be the name of a specific backup to mount
#   extract: (mandatory) arg[0] must be the backup to extract from, arg[1]
#   must be the file path to extract.
def create(
        runtype,
        subcommand, 
        *args
        ):
    # add command and subcommand
    full_command = ['borg']
    full_command.append(subcommand)
    # handle options differently based on subcommand
    if subcommand == 'list':
        # add repopath
        tmp = getattr(settings, 'repopath')
        # add folder path if it exists
        # append backup name if provided
        try:
            tmp2 = args[0]
            tmp = tmp + '::' + tmp2
        except IndexError:
            pass
        # append constructed command
        full_command.append(tmp)
    elif subcommand == 'mount':
        full_command.append(getattr(settings, 'repopath') + '::' + args[0])
        full_command.append(getattr(settings, 'mountpoint'))
        atexit.register(create, 'run', 'umount')
        # it may raise IndexError but this can only be raised by a bug anyway.
    elif subcommand == 'umount':
        full_command.append(getattr(settings, 'mountpoint'))
    elif subcommand == 'extract':
        # add backup to extract from
        full_command.append(getattr(settings, 'repopath') + '::' + args[0])
        # add file to extract
        full_command.append(args[1])
    
    # return based on runtype option
    if runtype.lower() == 'popen':
        return subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=dict(os.environ, BORG_PASSPHRASE=getattr(settings, 'passphrase'))
                )
    elif runtype.lower() == 'run':
        return subprocess.run( \
                full_command, \
                stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT, \
                env=dict(os.environ, BORG_PASSPHRASE=getattr(settings, 'passphrase'))
                )
    else:
        raise SyntaxError("no valid runtype found")

