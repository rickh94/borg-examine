# Borg Examine
This is an interactive python script for extracting files from borg backup
repos. It is intended to help users who are not familiar with CLIs (my family)
extract files from their backups without intervention as well as for anyone
who wants a little interactive help digging through their backups. Current
implementation stores repo password in clear text in a configuration file. If
you are not comfortable with this, you can use key-based authorization (check
borg's documentation for details).

## Installation Copy the repository to somewhere in your path and make
borg_examine.py executable or reference it with a shell script. I may generate
byte-code at some point but not at the moment.

## Configuration Configuration is handled by a borg-examine.conf held in
`$HOME/.config/borg-examine/`. You can edit the example provided or the script
will help you created one interactively if it is not found. If your user does
not have write access to the `.config` directory, it will raise an error.
Change the ownership or permissions and it will work correctly.

## Dependencies
* [python3](http://python.org)
* [Borg Backup](http://borgbackup.readthedocs.io/en/stable) - deduplicating
  backup program
* I make use of the `borg mount` command so fuse support is required:
    * Linux: usually native, check your distro
    * macOS: install [Fuse for macOS](http://osxfuse.github.io)
* You will also need the python3 llfuse package. Can be installed with `pip3
  install llfuse` *NOTE:* This package will not install if your system does
not have fuse support.

## Usage Currently the script presents the user with the times of all
available backups and mounts the selected one. You can then copy out any files
you need and it will unmount the backup at exit (as long as it closes
cleanly). If the wrong backup is mounted it can run continuously unmounting
and mounting backups until the user is finished. It is written to be mostly
self-explanatory.

NOTE: It is not advisable to run this script as root. It may look in the root
home directory for a config file and when it mounts the backup, your user will
not be able to access it without elevating privileges and files copied out may
have permission issues as well. If you MUST run it as root, consider becoming
root with `su -` or `sudo -s` instead of just running the script with sudo,
just don't break anything.

## Author
Frederic Henry fredericmhenry@gmail.com
