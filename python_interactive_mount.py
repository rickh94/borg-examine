#!/usr/bin/env python3
# interactive file recovery for borg backup

import os, subprocess, pprint, re, sys, datetime
my_repo = 'backup-test:borgmatic-test'
my_path = '/usr/bin/borg'
my_passphrase = 'testing123'

# backup class for storing/retrieving info about backups
class Backup:
    def __init__(self, name, date_time):
        self.name = name
        self.datetime = date_time


def backup_list(repo, borg_path, borg_passphrase):
    # get list from backup repo
    run = subprocess.run([borg_path, 'list', repo], \
            stdout=subprocess.PIPE, \
            env=dict(os.environ, BORG_PASSPHRASE=borg_passphrase))
    raw_list = run.stdout
    arr_list = raw_list.splitlines()
    return arr_list

def store_backup_info(backup_array):
    # store information about each backup in backup objects
    all_backups = []
    for backup in backup_array:
        decoded = backup.decode(sys.stdout.encoding)
        name = re.match("[^\s]*", decoded).group()
        raw_date = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', decoded).group()
        date_time = datetime.datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')
        tmp = Backup(name, date_time)
        all_backups.append(tmp)

    return all_backups

backups = store_backup_info(backup_list(my_repo, my_path, my_passphrase))
for b in backups: print(b.name, b.datetime)
