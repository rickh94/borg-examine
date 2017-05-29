#!/usr/bin/env python3
# borgstractor.py - main functions for interactive file recovery from borg backup archive. Borg backup is required.
# NOTE: When not properly shutdown, this will leave a backup mounted and the repository locked and further backups will
# not be possible until it is umounted. If placed on a system where backups are automated, a daemon or cron job should
# check periodically for mounted borgfs.

import os, subprocess, pprint, re, sys, datetime, atexit
import config
import get_backups
import narrow_down


# choose a backup to examine.
def choose_examine(backups):
    # auto return first backup if only one in array
    if len(backups) == 1:
        return 0
    # end if
    i = 0
    print("Backups are available from these times/dates: ")
    while i < len(backups):
        b = backups[i]
        # number and format for printing
        output = ['(' + str(i) + ')', b.pretty_date()]
        print("{:<4} {:<}".format(*output))
        i += 1
    # end while 
    number = input("Type the number of the backup you would like to examine. ")
    return int(number)
# end choose_examine


# cleanup mounted filesystem
def cleanup(mountpoint):
    subprocess.run(['borg', 'umount', mountpoint])
# end cleanup

# check if user found file and run again or exit.
def done(mountpoint, opencommand):
    print("Your backup is available at {}. It will now open for you to find the" \
            .format(mountpoint), 
            "files you need and copy them out of the backup. When you are done", 
            "please return to this window to close the backup.")
    # wait for user
    trash = input("Press [enter] to continue.")
    # open mounted directory
    subprocess.Popen([opencommand, mountpoint])
    while True:
        # return true or false for continuation or exit
        yn = input("Did you find what you were looking for?[y/n]")
        try:
            return bool(yn[0] == 'Y' or yn[0] == 'y')
        except IndexError:
            print("Please type [y]es or [n]o")
        # end try
    # end while
# end done


def main():
    # get configuration out of config file
    options = config.parseconfig()
    # cleanup function. Mounted backups will prevent any backups until unmount or reboot.
    # atexit.register(cleanup, options['mountpoint'])
    # get the actual backups
    all_backups = get_backups.backup_list(options['repopath'], options['passphrase']) 
    # store the backups nicely
    backups_clean = get_backups.parse_backup_info(all_backups)
    # narrow down the backups
    while True:
        # choose one backup to look at
        # NOTE: If list of backups is short enough, looping through all chosen backups may be viable.
        fewer = narrow_down.narrow_down(backups_clean)
        b = choose_examine(fewer)
        search_regex = get_backups.search_filename("Please enter the name of the file you are looking for: ")
        
        ret = fewer[b].extract_file(options, search_regex)
        if ret == 1:
            print("Returning to backups\n")
            continue

        """
        backups_clean[b].mount(options)
        """
        if done(options['mountpoint'], options['opencommand']):
            print("Great. Your backup is being unmounted.")
            break
        else:
            print("Let's try a different backup.")
            # cleanup(options['mountpoint'])
        # end if
    # end while
# end main

if __name__ == "__main__":
    main()
