#!/usr/bin/env python3
# narrow_down.py- module to hold function for narrowing down backups presented to the user.

import datetime
import settings

today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1))
last_week = (yesterday - datetime.timedelta(days=7))
last_year = (yesterday - datetime.timedelta(days=365))

def narrow_down(backups):
    # user input
    yn = input("There are a large number of backups available in your repository. " +
            "Would you like to narrow them down?[yn] ")
    while True:
        try:
            # return if the user wants to see full list
            if yn[0] == 'N' or yn[0] == 'n':
                return backups
            else:
                break
        except IndexError:
            yn = input("Please enter [y]es or [n]o.")
        # end try
    # end while
    
    while True:
        print("Would you like to see:")
        # dictionary of available options
        choices = {'1': 'Your most recent backup',
                '2': 'All backups from today',
                '3': 'All backups from yesterday',
                '4': 'All backups from the last week (not including today and yesterday),',
                '5': 'Backups from before last week',
                # '6': 'Backups from last year'
                }
            # 6 for debugging only
        # print options with keys
        for k, v in choices.items():
            print('(' + k + ')', v)
        # end printing loop
    # end while

        while True:
            choice = input("Please enter your choice: ")
            try:
                if choice[0] in choices:
                    break
                else:
                    print("Out of range.")
                # end validation if
            except IndexError:
                continue
            # end input validation try
        # end validation loop

        # dictionary of tests for choose function
        tests = {
                '2': 'today', 
                '3': 'yesterday', 
                '4': 'last week', 
                '5': 'older',
                # '6': 'last year'
                }
            # 6 for debugging only
        chosen = []
        try: 
            if choice == '1':
                # returns last backup aka most recent
                return [backups[-1]]
            else:
                for b in backups:
                    if choose(b, tests[choice]):
                        chosen.append(b)
                # end for (for adding chosen backups to array)
            # end if (chosing backups)
        except ValueError:
            print("Invalid input.")
            continue
        except IndexError:
            continue
        # end try



        # prevents empty list
        if len(chosen) == 0:
            print("\nNo backups available from that time. Please choose a different time.") 
        else:
            break
        # end available backups validation if


    return chosen


def choose(backup, test):
    # checks whether a backup meets the chosen condition
    if test == 'today':
        return bool(backup.date_time.date() == today)
    elif test == 'yesterday':
        return bool(backup.date_time.date() == yesterday)
    elif test == 'last week':
        return bool(yesterday > backup.date_time.date() > last_week)
    elif test == 'older':
        return bool(backup.date_time.date() < last_week)
    # elif test == 'last year':
    #     return bool(backup.date_time.date() < last_year)
    # end tests if
# end def choose
