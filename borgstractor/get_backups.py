#!/usr/bin/env python3
# class and functions for retrieving backup information.

import os
import subprocess
import datetime
import re
import sys
import shutil
import atexit
from borgstractor import borg_command
from borgstractor import settings

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
    def mount(self):
        # A nice message in case it takes a while
        print("Please wait a moment, your backup is being retrieved.")
        # create the mountpoint if it doesn't already exist
        if not os.path.exists(getattr(settings, 'mountpoint')): 
            os.mkdir(getattr(settings, 'mountpoint'))
        # mount the backup
        run = borg_command.create('run', 'mount', self.name)
    # end def mount

    def extract_file(
            self, 
            # file_regex
            ):
        # TODO: move all of this into a function
        # get list of files from backup
        make_list = borg_command.create('Popen', 'list', self.name)
        # store output and return code
        backup_list = make_list.communicate()[0].decode(sys.stdout.encoding),make_list.returncode

        # TODO: force it to sleep in case it is a timeout so that user doesn't
        # have to go through everything again. Or write progress to a file so
        # that it can be resumed from previous run.

        # catch errors
        if int(backup_list[1]) != 0: catch_borg_errors(backup_list)

        # searches for initial list of files, creates objects, prints, returns array
        file_list = backup_list[0].split('\n')
        found_files = search_filename('enter search', file_list)
        # print(found_files)
        # raw_files = find_files(backup_list[0], file_regex)
        all_files = parse_file_info(file_list)
        print(all_files)
        # NOTE: A lot of this flow control should be in the main function.
        # print_found_files(all_files)
        #
        # go_back = 0
        # new_files = []
        # # loop to validate input
        # while True:
        #     extract_response = input("Enter the number of the file/folder you would like to extract, or:\n"+
        #             "\tsearch [W]ithin results,\n\tperform a [N]ew search of this backup\n" +
        #             "\ttemporarily [M]ount this backup\n\tor check a different [B]ackup.\n")
        #     # try to extract file at index, if other choice was made, error is raised and block is skipped
        #     try:
        #         # file indicies were printed offset by 1 so they don't start
        #         # at 0. This just removes that offset so the inidicies line up
        #         # with the list again.
        #         file_num = int(extract_response) - 1
        #         # reset loop if file_num is not proper index
        #         if not file_num < len(all_files):
        #             print("Invalid input.")
        #             continue
        #         else:
        #             print("Extracting your file...")
        #         # end if
        #         # extract from new_files it present
        #         self.extract(file_num, all_files)
        #         # check if file is correct and try again return failure or go back somewhere in loop
        #         done = input("Would you like to:\n\textract a different [F]ile from this backup\n\t" +
        #                 "extract a file from a [D]ifferent " +
        #                 "backup\n\t[E]xit this program\n")
        #         while True:
        #             try:
        #                 if done[0] == 'F' or done[0] == 'f':
        #                     tmp_list = backup_list[0]
        #                     new_files, all_files = new_search(tmp_list)
        #                     go_back = 1
        #                     break
        #                 # different backup
        #                 elif done[0] == 'D' or done[0] == 'd':
        #                     return 1
        #                 # done. exit
        #                 elif done[0] == 'E' or done[0] == 'e':
        #                     return 0
        #                 else:
        #                     done = input("Please enter your selection ")
        #                     continue
        #                 # end if
        #             except IndexError:
        #                 continue
        #             # end try
        #         if go_back == 1:
        #             continue
        #
        #     # executes if input is not int
        #     except ValueError:
        #         try:
        #             # new search
        #             if extract_response[0] == 'N' or extract_response == 'n':
        #                 tmp_list = backup_list[0]
        #                 new_files, all_files = new_search(tmp_list)
        #                 # go back to extract response and try again
        #                 continue
        #
        #             # returns failure and a different backup can be selected
        #             elif extract_response[0] == 'B' or extract_response == 'b':
        #                 print("Returning to backup selection.")
        #                 return 1
        #             elif extract_response[0] == 'W' or extract_response[0] == 'w':
        #                 # search within
        #                 search_regex = search_filename("Please enter an additional search term (a parent folder or " +
        #                         "file extension can narrow it down a lot): ")
        #                 # if this is not the second search performed, new_files will exist and we should search within that
        #                 # in either case, join the array of raw file info back into a single text string so that the
        #                 # original search function will work.
        #                 if new_files:
        #                     new_files = find_files("\n".join(new_files), search_regex)
        #                 else:
        #                     new_files = find_files("\n".join(raw_files), search_regex)
        #
        #                 all_files = parse_file_info(new_files)
        #                 print_found_files(all_files)
        #                 # back around for another pass
        #                 continue
        #
        #             elif extract_response[0] == 'M' or extract_response == 'm':
        #                 # mount that backup
        #                 self.mount()
        #                 done = done_mounting(getattr(settings, 'mountpoint'), getattr(settings, 'opencommand'))
        #                 if done:
        #                     return 0
        #                     # exits the program
        #                 else:
        #                     cleanup(getattr(settings, 'mountpoint'))
        #                     return 1
        #                     # returns to backup selection
        #             else:
        #                 print("Invalid input")
        #                 continue
        #         except IndexError:
        #             print("Please enter a response.")
        #             continue
        #     else:
        #         # catastrophic problem. should never happen. kills program.
        #         print("Something has gone wrong.")
        #         sys.exit(1)
                # end if / elif for non-number input
            # end try (for user input)
        # end while (user input)
    # end def extract_file

    def extract(self, num, file_list):
        to_extract = file_list[num]

        # make extraction dir if not found and change to it
        ext_dir = getattr(settings, 'extractdir')
        if not os.path.exists(ext_dir): os.mkdir(ext_dir)

        os.chdir('/tmp')
        # extract the file and rename it
        borg_command.create('run', 'extract', self.name, to_extract.name)

        full_extract = '/tmp/' + to_extract.name
        extracted_file_name = os.path.basename(full_extract)
        shutil.move(full_extract, ext_dir + '/' + to_extract.date_time.strftime("%Y-%m-%d_%H:%M:%S-") + extracted_file_name)

        # wait for user confirmation to open restored file
        trash = input("Press [enter] to see your extracted file.")
        subprocess.Popen([getattr(settings, 'opencommand'), ext_dir])


# end Backup class


class FoundFile(DatedInfo):
    pass

########## FILE FUNCTIONS SECTION ############ 
def search_filename(message, list_of_files): 
    # get input and clean it for use in regex 
    while 1:
        filename = input(message)
        if filename != '':
            break
        else:
            print("No input detected")
    # end while (for input validation)

    # filename = re.escape(filename.strip())
    # ret_list = []
    # for line in list_of_files:
    #     if filename in line:
    #         ret_list.append(line.strip())

    # comprehension
    ret_list = [line for line in list_of_files if (filename in line
        and ' -> ' not in line)]

    return ret_list

    # file_regex = re.compile(r"^.*?" + filename + r".*?$", flags=re.IGNORECASE|re.MULTILINE)
    # print("\nSeaching for your file (this could take a while)...")
    # return file_regex
# end def search_filename

def parse_file_info(file_array):
    all_files = []
    for f in file_array:
        if f is '':
            continue
        if ' -> ' in f:
            continue
        # find date
        raw_date = re.search(r'\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', f).group()
        date_time = datetime.datetime.strptime(raw_date, ' %Y-%m-%d %H:%M:%S')
        # find name after date
        find_name = re.search(r':\d{2}\s.*', f).group()
        # drop date part of regex
        name = find_name[4:]
        # ignore symlinks
        all_files.append(FoundFile(name, date_time))
    # end for loop (making objects from array)
    return all_files
# end def parse_file_info


########## BACKUP FUNCTIONS SECTIONS ############
def backup_list():
    # get list from backup repo
    run = borg_command.create('Popen', 'list')
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

        # ignore checkpoints
        if re.match(".*\.checkpoint", name) is None:
            tmp = Backup(name, date_time)
            all_backups.append(tmp)
        # add backup object to list
    # end for loop (storing info)

    return all_backups
# end def parse_backup_info

# cleanup mounted filesystem
def cleanup(mountpoint):
    subprocess.run(['borg', 'umount', mountpoint])
# end cleanup

# check if user found file and run again or exit.
def done_mounting(mountpoint, opencommand):
    print("Your backup is available at {}. It will now open for you to find the" \
            .format(mountpoint), 
            "files you need and copy them out of the backup. When you are done", 
            "please return to this window to close the backup.")
    # wait for user
    trash = input("Press [enter] to continue.")
    # open mounted directory
    subprocess.Popen([opencommand, mountpoint])
    while True:
        # return true or false for continuation or exit
        yn = input("Did you find what you were looking for?[y/n]")
        try:
            return bool(yn[0] == 'Y' or yn[0] == 'y')
        except IndexError:
            print("Please type [y]es or [n]o")
        # end try
    # end while
# end done

def find_files(file_list, regex):
    while 1:
        raw_files = regex.findall(str(file_list))
        if len(raw_files) == 0:
            regex = search_filename("No matches found. Please enter a new" +
                    " search: ")
        else:
            break
    return raw_files

def print_found_files(file_list):
    print("Here are the files that match your search in the chosen backup.")
    i = 0
    # print out files
    while i < len(file_list):
        f = file_list[i]
        # offset i for printing and better UX
        output = ['(' + str(i + 1) + ')', f.name, 'LAST MODIFIED ' + f.pretty_date()]
        print("{:<4} {:<90} {:>10}".format(*output))
        i += 1
    # end while (printing files)
# end def print_found_files

def new_search(raw_file_list):
    search_regex = search_filename("\nPlease enter a new search term: ")
    new_files = find_files(raw_file_list, search_regex)
    all_files = parse_file_info(new_files)
    print_found_files(all_files)
    return new_files, all_files

######## ERROR HANDLING FUNCTIONS #########
def catch_borg_errors(ret):
    # possible problems created running borg list. Hack-y, but it works.
    messages = {
            'LockTimeout': 'Cannot unlock repository. Backup may be in progress. Try again in a few minutes.',
            'passphrase': 'Passphrase was rejected. Update config file and try again.',
            'valid': 'The repository in your config file does not appear to be valid. Please correct it.',
            'exist': 'The repository in your config file does not exist. Please correct.',
            'remote': 'Connection to backup server failed. Check network connection.',
            'other': 'An unknown error has occurred. Printing borg traceback:\n' + ret[0] 
            }
    # check for possible issues and raise an error if they arise.
    for k, v in messages.items():
        if k in ret[0]: raise AccessError(v)
    # end for loop to raise error
# end def catch_borg_errors

