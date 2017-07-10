# Borgstractor
This is an interactive python script for extracting files from borg backup
repos. It is intended to help users who are not familiar with CLIs (my family)
extract files from their backups without intervention as well as for anyone
who wants a little interactive help digging through their backups. Current
implementation stores repo password in clear text in a configuration file. If
you are not comfortable with this, you can use key-based authentication (check
borg's documentation for details).

## Installation 
```shell
$ git clone https://github.com/rickh94/borgstractor.git
$ cd borgstractor
# python3 setup.py install
```

This is a wrapper script for [Borg
Backup](http://borgbackup.readthedocs.io/en/stable) which only supports
unix-like operating systems, so this script only supports unix-like operating
systems.

## Configuration 
Configuration is handled by a borgstractor.conf held in
`$HOME/.config/borgstractor/`. You can edit the example provided or the script
will help you created one interactively if it is not found. If your user does
not have write access to the `.config` directory, it will raise an error.
Change the ownership or permissions and it will work correctly.  
The location of the config file is hard coded so if you don't like it, edit
the source code.

## Dependencies
* [python3](http://python.org)
* [Borg Backup](http://borgbackup.readthedocs.io/en/stable) - deduplicating
  backup program
* (optional) I make use of the `borg mount` command so fuse support is required:
    * Linux: usually native, check your distro
    * macOS: install [Fuse for macOS](http://osxfuse.github.io)
* You will also need the python3 llfuse package. Can be installed with `pip3
  install llfuse` *NOTE:* This package will not install if your system does
not have fuse support.

## Usage 
The program itself is fairly self-explanatory, follow the directions on the
screen. The configuration file is generated interactively if not found. The
more information you have about a file (path, name, modification date), the
easier it will be to find.

NOTE: It is not advisable to run this script as root. It may look in the root
home directory for a config file and when it mounts the backup, your user will
not be able to access it without elevating privileges and files copied out may
have permission issues as well. If you MUST run it as root, consider becoming
root with `su -` or `sudo -s` instead of just running the script with sudo,
just don't break anything.

## Features
* Search a backup for a specific file and search within results to narrow down
  further.
* Mount an entire backup to examine it manually.
* Extract multiple files, perform multiple searches in one session.
* Select from narrowed list of backups based on time created.


## Author
Rick Henry fredericmhenry@gmail.com
