#!/usr/bin/env python3
# class and functions for retrieving backup information.

import os, subprocess, datetime, re, sys

# Exception raised when borg list is not successfully completed.
class AccessError(Exception):
    pass

# Class for storing information about backups in a repo.
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
        # A nice message in case it takes a while
        print("Please wait a moment, your backup is being retrieved.")
        # create the mountpoint if it doesn't already exist
        if not os.path.exists(options['mountpoint']):
            os.mkdir(options['mountpoint'])
        run = subprocess.run(['borg', 'mount', options['repopath'] + '::' + self.name, 
            options['mountpoint']], env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))

    def extract_file(self, options, file_regex):
        # get list of files from backup
        make_list = subprocess.Popen(['borg', 'list', options['repopath'] + '::' + self.name], \
                stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT, \
                env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))
        # store output and return code
        backup_list = make_list.communicate()[0].decode(sys.stdout.encoding),make_list.returncode
        # TODO: force it to sleep in case it is a timeout so that user doesn't
        # have to go through everything again. Or write progress to a file so
        # that it can be resumed from previous run.
        # catch errors
        if int(backup_list[1]) != 0: catch_borg_errors(backup_list)
        files = file_regex.findall(str(backup_list[0]))
        print("Here are the files that match your search in the chosen backup.")
        for f in files:
            print(f)

def get_filename():
    # get input and clean it for use in regex
    filename = input("Please enter all or part of the filename you are looking for: ")
    filename = re.escape(filename.strip())
    # create regex that will return entire line from borg list based on user input
    file_regex = re.compile(r"^.*?" + filename + r".*?$", flags=re.IGNORECASE|re.MULTILINE)
    return file_regex


def backup_list(repopath, passphrase):
    # get list from backup repo
    run = subprocess.Popen(['borg', 'list', repopath], \
            stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT, \
            env=dict(os.environ, BORG_PASSPHRASE=passphrase))
    ret = run.communicate()[0].decode(sys.stdout.encoding),run.returncode
    # stop program if list doesn't properly get a list
    if int(ret[1]) != 0: catch_borg_errors(ret)
    arr_list = ret[0].splitlines()
    # return array, at this point just a text dump of each backup
    return arr_list

def catch_borg_errors(ret):
    # possible problems created running borg list. Hack-y, but it works.
    messages = {
            'LockTimeout': 'Cannot unlock repository. Backup may be in progress. Try again in a few minutes.',
            'passphrase': 'Passphrase was rejected. Update config file and try again.',
            'valid': 'The repository in your config file does not appear to be valid. Please correct it.',
            'exist': 'The repository in your config file does not exist. Please correct.',
            'remote': 'Connection to backup server failed. Check network connection.',
            'other': 'An unknown error has occurred: ' + ret[0] 
            }
    # check for possible issues and raise an error if they arise.
    for k, v in messages.items():
        if k in ret[0]: raise AccessError(v)


def parse_backup_info(backup_array):
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

    # now they're nice objects
    return all_backups
