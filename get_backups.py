#!/usr/bin/env python3
# class and functions for retrieving backup information.

import os, subprocess, datetime, re, sys

class Backup:
    def __init__(self, name, date_time):
        self.name = name
        self.date_time = date_time

    # human readable date for printing
    def pretty_date(self):
        if self.date_time.date() == datetime.date.today():
            return str(self.date_time.strftime("Today at %I:%M %p"))
        elif self.date_time.date() == (datetime.date.today() - datetime.timedelta(days=1)):
            return str(self.date_time.strftime("Yesterday at %I:%M %p"))
        else:
            return str(self.date_time.strftime("%a, %b %d, %Y at %I:%M %p"))

    # mount the backup.
    def mount(self, options):
        print("Please wait a moment, your backup is being retrieved.")
        if not os.path.exists(options['mountpoint']):
            os.mkdir(options['mountpoint'])
        run = subprocess.run(['borg', 'mount', options['repopath'] + '::' + self.name, 
            options['mountpoint']], env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))

def backup_list(repopath, passphrase):
    # get list from backup repo
    run = subprocess.Popen(['borg', 'list', repopath], \
            stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT, \
            env=dict(os.environ, BORG_PASSPHRASE=passphrase))
    # raw_list = run.stdout
    ret = run.communicate()[0].decode(sys.stdout.encoding),run.returncode
    if int(ret[1]) != 0:
        print("Something has gone wrong:")
        if "LockTimeout" in ret[0]:
            print("Lock Error: Your system may be performing a backup.",
            "Please try again in a few minutes.")
            sys.exit(1)
        elif "passphrase" in ret[0]:
            print("Passphrase Error: Check that your passphrase is correct in your config file and try again.",
                    "You can also delete the config file and a new one will be created next time you run this program.")
            sys.exit(1)
        elif "valid" in ret[0]:
            print("Repository Error: Check that the repository path is correct in your config file and",
                    "try again. You can also delete the config file and a new one will be",
                    "created next time you run this program.")
            sys.exit(1)
        elif "remote" in ret[0]:
            print("Server Error: Check your connection to your backup server and try again.")
            sys.exit(1)
        else:
            print("An unknown error has occurred. Details follow:")
            print(ret[0])
            sys.exit(1)
    arr_list = ret[0].splitlines()
    return arr_list


def store_backup_info(backup_array):
    # store information about each backup in backup objects
    all_backups = []
    for backup in backup_array:
        # parse backup info
        name = re.match("[^\s]*", backup).group()
        raw_date = re.search(r'\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', backup).group()
        date_time = datetime.datetime.strptime(raw_date, ' %Y-%m-%d %H:%M:%S')

        # add backup object to list
        tmp = Backup(name, date_time)
        all_backups.append(tmp)

    return all_backups
