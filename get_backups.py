#!/usr/bin/env python3
# class and functions for retrieving backup information.

import os, subprocess, datetime, re, sys, shutil

######## CLASSES SECTION ##########

# Exception raised when borg list is not successfully completed.
class AccessError(Exception):
    pass

class DatedInfo:
    def __init__(self, name, date_time):
        self.name = name
        self.date_time = date_time
    # end def __init__

    # human readable date for printing
    def pretty_date(self):
        if self.date_time.date() == datetime.date.today():
            return str(self.date_time.strftime("Today at %I:%M %p"))
        elif self.date_time.date() == (datetime.date.today() - datetime.timedelta(days=1)):
            return str(self.date_time.strftime("Yesterday at %I:%M %p"))
        else:
            return str(self.date_time.strftime("%a, %b %d, %Y at %I:%M %p"))
        # end if
    # end def pretty_date
# end class DatedInfo

# Class for storing information about backups in a repo.
class Backup(DatedInfo):
    # mount the backup.
    def mount(self, options):
        # A nice message in case it takes a while
        print("Please wait a moment, your backup is being retrieved.")
        # create the mountpoint if it doesn't already exist
        if not os.path.exists(options['mountpoint']): os.mkdir(options['mountpoint'])
        # mount the backup
        run = subprocess.run(['borg', 'mount', options['repopath'] + '::' + self.name, 
            options['mountpoint']], env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))
    # end def mount

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

        # TODO: loop for drill down search probably needs to start here. may need to move call to generate search inside
        # this function.
        # create FoundFile objects
        all_files = print_found_files(backup_list[0], file_regex)

        # loop to validate input
        while True:
            extract_response = input("Enter the number of the file you would like to extract, or you can [S]earch again or " +
                    "Check another [B]ackup. ")
            # try to extract file at index, if other choice was made, error is raised and block is skipped
            try:
                file_num = int(extract_response)
                # reset loop if file_num is not proper index
                if not file_num < len(all_files):
                    print("Invalid input.")
                    continue
                else:
                    print("Extracting your file...")
                # end if
                to_extract = all_files[file_num]
                # make extraction dir if not found and change to it
                ext_dir = options['extractdir']
                if not os.path.exists(ext_dir): os.mkdir(ext_dir)
                os.chdir('/tmp')
                # extract the file and rename it
                subprocess.run(['borg', 'extract', options['repopath'] + '::' + self.name, to_extract.name], \
                        env=dict(os.environ, BORG_PASSPHRASE=options['passphrase']))
                full_extract = '/tmp/' + to_extract.name
                extracted_file_name = os.path.basename(full_extract)
                shutil.move(full_extract, ext_dir + '/' + to_extract.date_time.strftime("%Y-%m-%d_%H:%M:%S-") + extracted_file_name)
                # wait for user confirmation to open restored file
                trash = input("Press [enter] to see your extracted file.")
                subprocess.run([options['opencommand'], ext_dir])
                # check if file is correct and try again return failure or go back somewhere in loop
                # return success
                break
            # executes if input is not int
            except ValueError:
                print("That's not ready yet, sorry")
                """
                if extract_response[0] == 'S' or extract_response == 's':
                    # go back to parse_file_info and try again (enclose even more shit in a loop)
                elif extract_response[0] == 'B' or extract_response == 'b':
                    # return failure and go back to backups
                # possibly also accept switching to mounting through different return code
                """
            # end try (for user input)
        # end while (user input)
    # end def extract_file
# end Backup class


                

class FoundFile(DatedInfo):
    pass

########## FILE FUNCTIONS SECTION ############ 
def search_filename(): 
    # get input and clean it for use in regex 
    filename = input("Please enter all or part of the filename you are looking for: ")
    filename = re.escape(filename.strip())
    # create regex that will return entire line from borg list based on user input
    file_regex = re.compile(r"^.*?" + filename + r".*?$", flags=re.IGNORECASE|re.MULTILINE)
    print("\nSeaching for your file...")
    return file_regex
# end def search_filename

def parse_file_info(file_array):
    all_files = []
    for f in file_array:
        # fine date
        raw_date = re.search(r'\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', f).group()
        date_time = datetime.datetime.strptime(raw_date, ' %Y-%m-%d %H:%M:%S')
        # find name after date
        find_name = re.search(r':\d{2}\s.*', f).group()
        # drop date part of regex
        name = find_name[4:]
        all_files.append(FoundFile(name, date_time))
    # end for loop (making objects from array)
    return all_files
# end def parse_file_info


########## BACKUP FUNCTIONS SECTIONS ############
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
# end def backup_list


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
    # end for loop (storing info)

    return all_backups
# end def parse_backup_info
def print_found_files(file_list, regex):
    raw_files = regex.findall(str(file_list))
    all_files = parse_file_info(raw_files)
    print("\nHere are the files that match your search in the chosen backup.")
    i = 0
    # print out files
    while i < len(all_files):
        f = all_files[i]
        # number and format for printing
        output = ['(' + str(i) + ')', f.name, 'LAST MODIFIED ' + f.pretty_date()]
        print("{:<4} {:<90} {:>10}".format(*output))
        i += 1
    return all_files
    # end while (printing files)
# end def print_found_files

######## ERROR HANDLING FUNCTIONS #########
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
    # end for loop to raise error
# end def catch_borg_errors

