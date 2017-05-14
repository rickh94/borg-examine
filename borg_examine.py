#!/usr/bin/env python3
# interactive file recovery for borg backup
# NOTE: When not properly shutdown, this will leave a backup mounted and the repository locked and further backups will
# not be possible until it is umounted. If placed on a system where backups are automated, a daemon or cron job should
# check periodically for mounted borgfs.

import os, subprocess, pprint, re, sys, datetime, atexit
import config
import get_backups


# choose a backup to examine.
def choose_examine(backups):
    i = 0
    print("Backups are available from these times/dates: ")
    for b in backups:
        output = ['(' + str(i) + ')', b.pretty_date()]
        print('{:>4} {:<}'.format(*output))
        i += 1
    number = input("Type the number of the backup you would like to examine. ")
    return int(number)


# cleanup mounted filesystem
def cleanup(mountpoint):
    subprocess.run(['borg', 'umount', mountpoint])

# check if user found file and run again or exit.
def done(mountpoint):
    print("Your backup is available at {}. Please copy any files and return to this program"\
            .format(mountpoint))
    while True:
        yn = input("Did you find what you were looking for?[y/n]")
        try:
            return bool(yn[0] == 'Y' or yn[0] == 'y')
        except IndexError:
            print("Please type [y]es or [n]o")


def main():
    options = config.parseconfig()
    atexit.register(cleanup, options['mountpoint'])
    all_backups = get_backups.backup_list(options['repopath'], options['passphrase']) 
    backups_clean = get_backups.store_backup_info(all_backups)
    while True:
        b = choose_examine(backups_clean)
        backups_clean[b].mount(options)
        if done(options['mountpoint']):
            print("Great. Your backup is being unmounted.")
            break
        else:
            print("Let's try a different backup.")
            cleanup(options['mountpoint'])

if __name__ == "__main__":
    main()
