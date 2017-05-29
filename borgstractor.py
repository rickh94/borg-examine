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


def main():
    # get configuration out of config file
    options = config.parseconfig()

    # get the actual backups
    all_backups = get_backups.backup_list(options['repopath'], options['passphrase']) 

    # store the backups nicely
    backups_clean = get_backups.parse_backup_info(all_backups)

    while True:
        # choose one backup to look at
        # narrow down the backups
        fewer = narrow_down.narrow_down(backups_clean)
        b = choose_examine(fewer)
        search_regex = get_backups.search_filename("Please enter the name of the file you are looking for: ")
        
        ret = fewer[b].extract_file(options, search_regex)
        if ret == 1:
            print("Returning to backups\n")
            continue
        elif ret == 0:
            print("Have a nice day")
            break

    # end while
# end main

if __name__ == "__main__":
    main()
