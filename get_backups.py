#!/usr/bin/env python3
# class and functions for retrieving backup information.

import os, subprocess, datetime, re, sys

class AccessError(Exception):
    pass

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

def catch_borg_errors(ret):
    messages = {
            'LockTimeout': 'Cannot unlock repository. Backup may be in progress. Try again in a few minutes.',
            'passphrase': 'Passphrase was rejected. Update config file and try again.',
            'valid': 'The repository in your config file does not appear to be valid. Please correct it.',
            'exist': 'The repository in your config file does not exist. Please correct.',
            'remote': 'Connection to backup server failed. Check network connection.',
            'other': 'An unknown error has occurred: ' + ret[0] 
            }
    for k, v in messages.items():
        if k in ret[0]: raise AccessError(messages[k])


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
