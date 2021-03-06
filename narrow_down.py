#!/usr/bin/env python3
# narrow_down.py- module to hold function for narrowing down backups presented to the user.

import datetime

today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1))
last_week = (yesterday - datetime.timedelta(days=7))

def narrow_down(backups):
    # user input
    yn = input("There are a large number of backups available in your repository. " +
            "Would you like to narrow them down?[yn]")
    while True:
        try:
            # return if the user wants to see full list
            if yn[0] == 'N' or yn[0] == 'n':
                return backups
            else:
                break
        except IndexError:
            yn = input("Please enter [y]es or [n]o.")
    
    while True:
        print("Would you like to see:")
        # dictionary of available options
        choices = {'1': 'Your most recent backup',
                '2': 'All backups from today',
                '3': 'All backups from yesterday',
                '4': 'All backups from the last week (not including today and yesterday),',
                '5': 'Backups from before last week' }
        # print options with keys
        for k, v in choices.items():
            print('(' + k + ')', v)

        while True:
            choice = input("Please enter your choice: ")
            if choice[0] in choices:
                break
            else:
                print("Out of range.")

        # dictionary of tests for choose function
        tests = {'2': 'today', '3': 'yesterday', '4': 'last week', '5': 'older'}
        chosen = []
        if choice == '1':
            # returns last backup aka most recent
            return [backups[-1]]
        else:
            for b in backups:
                if choose(b, tests[choice]):
                    chosen.append(b)
        # prevents empty list
        if len(chosen) == 0:
            print("No backups available from that time. Please choose a different time.") 
        else:
            break


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
