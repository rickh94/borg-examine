#!/usr/bin/env python3
# interactive file recovery for borg backup
# NOTE: When not properly shutdown, this will leave a backup mounted and the repository locked and further backups will
# not be possible until it is umounted. If placed on a system where backups are automated, a daemon or cron job should
# check periodically for mounted borgfs.

import os, subprocess, pprint, re, sys, datetime, atexit
import config

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
    def mount(self, options):
        if not os.path.exists(options['mountpoint']):
            os.mkdir(options['mountpoint'])
        run = subprocess.run(['borg', 'mount', options['repopath'] + '::' + self.name, options['mountpoint']], \
                env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))

def backup_list(repopath, passphrase):
    # get list from backup repo
    run = subprocess.run(['borg', 'list', repopath], \
            stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, \
            env=dict(os.environ, BORG_PASSPHRASE=passphrase))
    raw_list = run.stdout.decode(sys.stdout.encoding)
    if "LockTimeout" in run.stderr.decode(sys.stderr.encoding):
        print("Cannot unlock repository: Your system may be performing a backup. Please try again in a few minutes.")
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
    all_backups = backup_list(options['repopath'], options['passphrase']) 
    backups_clean = store_backup_info(all_backups)
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
