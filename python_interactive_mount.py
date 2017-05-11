#!/usr/bin/env python3
# interactive file recovery for borg backup

# TODO: import config file (borrow borgmatic's code).
# TODO: automatically perform umount on exit
# TODO: prune down available backups interactively.
# TODO: functions for finding and extracting single file.
import os, subprocess, pprint, re, sys, datetime
repo = 'backup-test:borgmatic-test'
borg_path = '/usr/bin/borg'
borg_passphrase = 'testing123'
my_mountpoint = '/home/rick/recover_mount'

# backup class for storing/retrieving info about backups
class Backup:
    def __init__(self, name, date_time):
        self.name = name
        self.date_time = date_time

    def pretty_date(self):
        if self.date_time.date() == datetime.date.today():
            return str(self.date_time.strftime("Today at %I:%M %p"))
        elif self.date_time.date() == (datetime.date.today() - datetime.timedelta(days=1)):
            return str(self.date_time.strftime("Yesterday at %I:%M %p"))
        else:
            return str(self.date_time.strftime("%a, %b %d, %Y at %I:%M %p"))

    def mount(self, mount_point):
        run = subprocess.run([my_path, 'mount', repo + '::' + self.name, mount_point], \
                env=dict(os.environ, BORG_PASSPHRASE=my_passphrase))


def backup_list():
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
        # parse backup info
        decoded = backup.decode(sys.stdout.encoding)
        name = re.match("[^\s]*", decoded).group()
        raw_date = re.search(r'\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', decoded).group()
        date_time = datetime.datetime.strptime(raw_date, ' %Y-%m-%d %H:%M:%S')

        # add backup object to list
        tmp = Backup(name, date_time)
        all_backups.append(tmp)

    return all_backups


def choose_examine(backups):
    i = 0
    print("Backups are available from these times/dates: ")
    for b in backups:
        output = ['(' + str(i) + ')', b.pretty_date()]
        print('{:>4} {:<}'.format(*output))
        i += 1
    number = input("Type the number of the backup you would like to examine. ")
    backups[int(number)].mount(my_mountpoint)


backups = store_backup_info(backup_list())
# for b in backups: b.pretty_date
choose_examine(backups)
# for b in backups: print(b.name, b.datetime)

