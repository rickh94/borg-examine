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
    ret = run.communicate()[0].decode(sys.stdout.encoding),run.returncode
    if int(ret[1]) != 0: catch_borg_errors(ret)
    arr_list = ret[0].splitlines()
    return arr_list

# TODO: change into Exception classes and use raise to raise them.
def catch_borg_errors(ret):
        if "LockTimeout" in ret[0]:
            error = "LockError"
            message = "Your system may be performing a backup. " +\
                    "Please try again in a few minutes."
        elif "passphrase" in ret[0]:
            error = "PassphraseError"
            message = "Check that your passphrase is correct in your config file and try again. " +\
                    "You can also delete the config file and a new one will be created next time you run this program."
        elif "valid" in ret[0]:
            error = "RepositoryError"
            message = "Check that the repository path is correct in your config file and " +\
                    "try again. You may also delete the config file and a new one will be " +\
                    "created next time you run this program."
        elif "remote" in ret[0]:
            error = "ServerError"
            message = "Check your connection to your backup server and try again."
        else:
            error = "UnknownError"
            message = "An unknown error has occurred. The error message from borg follows:\n" + ret[0]
        print(error + ':', message)
        sys.exit(1)


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
