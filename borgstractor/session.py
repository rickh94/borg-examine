# Shelves session for use later that same day. deletes old sessions.
import os, shelve, datetime, glob
import settings
# from borgmatic import settins

home = os.path.expanduser("~")
now = datetime.datetime.now().strftime("%Y-%m-%d")
sess_prefix = home + '/.config/borgstractor/session-' 
sess_path = sess_prefix + now

def open_session():
    sess_exists = glob.glob(sess_prefix + '*')
    if sess_exists && !os.path.exists(sess_path):
        for a_file in sess_exists:
            os.remove(a_file)

    setattr(settings, session, shelve.open(sess_path))



