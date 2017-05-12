#!/usr/bin/env python3
# interactive file recovery for borg backup
# NOTE: When not properly shutdown, this will leave a backup mounted and the repository locked and further backups will
# not be possible until it is umounted. If placed on a system where backups are automated, a daemon or cron job should
# check periodically for mounted borgfs.

# TODO: import config file (borrow borgmatic's code).

# TODO: rescue failure to break lock
# TODO: prune down available backups interactively.
# TODO: functions for finding and extracting single file.
import os, subprocess, pprint, re, sys, datetime, atexit
repo = 'backup-test:borgmatic-test'
borg_path = '/usr/bin/borg'
borg_passphrase = 'testing123'
my_mountpoint = '/home/rick/recover_mount'

# backup class for storing/retrieving info about backups
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
    def mount(self, mount_point):
        run = subprocess.run([borg_path, 'mount', repo + '::' + self.name, mount_point], \
                env=dict(os.environ, BORG_PASSPHRASE=borg_passphrase))


def backup_list():
    # get list from backup repo
    run = subprocess.run([borg_path, 'list', repo], \
            stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, \
            env=dict(os.environ, BORG_PASSPHRASE=borg_passphrase))
    raw_list = run.stdout.decode(sys.stdout.encoding)
    if "LockTimeout" in run.stderr.decode(sys.stderr.encoding):
        # TODO: mount cleanup function here possibly
        print("Cannot unlock repository. Your system may be performing a backup. Try again in a few minutes.")
        sys.exit(1)
    arr_list = raw_list.splitlines()
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


def choose_examine(backups):
    i = 0
    print("Backups are available from these times/dates: ")
    for b in backups:
        output = ['(' + str(i) + ')', b.pretty_date()]
        print('{:>4} {:<}'.format(*output))
        i += 1
    number = input("Type the number of the backup you would like to examine. ")
    backups[int(number)].mount(my_mountpoint)

def cleanup():
    subprocess.run([borg_path, 'umount', my_mountpoint])

def done():
    print("Your backup is available at", str(my_mountpoint) + '.', "Please copy any files and return to this program")
    while True:
        yn = input("Did you find what you were looking for?[y/n]")
        try:
            return bool(yn[0] == 'Y' or yn[0] == 'y')
        except IndexError:
            print("Please type [y]es or [n]o")


atexit.register(cleanup)
backups = store_backup_info(backup_list())
while True:
    choose_examine(backups)
    if done():
        print("Great. Your backup is being unmounted.")
        break
    else:
        print("Let's try a different backup.")
        cleanup()
