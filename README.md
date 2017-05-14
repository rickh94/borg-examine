## Borg Examine
This is an interactive python script for extracting files from borg backup
repos.

# Installation
Copy the repository to somewhere in your path and make borg_examine.py
executable or reference it with a shell script.

# Configuration
Configuration is handled by a borg-examine.conf held in
$HOME/.config/borg-examine/. You can edit the example provided or the script
will help you created one interactively if it is not found.

# Usage
Currently the script presents the user with the times of all available backups
and mounts the selected one. You can then copy out any files you need and it
will unmount the backup at exit (as long as it closes cleanly). If the wrong
backup is mounted it can run continuously unmounting and mounting backups
until the user is finished.
