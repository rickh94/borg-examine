#!/usr/bin/env python3
# narrow down backups

import datetime

today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1))
last_week = (yesterday - datetime.timedelta(days=7))

def narrow_down(backups):
    yn = input("There are a large number of backups available in your repository. " +
            "Would you like to narrow them down?[yn]")
    while True:
        try:
            if yn[0] == 'N' or yn[0] == 'n':
                return backups
            else:
                break
        except IndexError:
            yn = input("Please enter [y]es or [n]o.")
    
    print("Would you like to see:")
    print("(1) Your most recent backup,")
    print("(2) All backups from today,")
    print("(3) All backups from yesterday,")
    print("(4) All backups from the last week (not including today and yesterday),")
    print("(5) Backups from before last week.")
    choice = input("")
    # this needs to capture exceptions and out of range choices
    tests = {'2': 'today', '3': 'yesterday', '4': 'last week', '5': 'older'}
    chosen = []
    if choice == '1':
        return [backups[-1]]
    else:
        for b in backups:
            if choose(b, tests[choice]):
                chosen.append(b)

    return chosen


def choose(backup, test):
    if test == 'today':
        return bool(backup.date_time.date() == today)
    elif test == 'yesterday':
        return bool(backup.date_time.date() == yesterday)
    elif test == 'last week':
        return bool(yesterday > backup.date_time.date() > last_week)
    elif test == 'older':
        return bool(backup.date_time.date() < last_week)
