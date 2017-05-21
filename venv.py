import os

# console-calendar requirement
import time
import argparse
import urllib

# string_cleanup requirement
import re
from datetime import datetime, timedelta
from collections import OrderedDict

# virtualenv
SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))

try:
    # googleoauth.py requirement
    from oauth2client import file, client, tools
    from httplib2 import Http
    from apiclient.discovery import build
except ImportError:
    venv_name = '_ccal'
    osdir = 'Scripts' if os.name is 'nt' else 'bin'
    venv = os.path.join(venv_name, osdir, 'activate_this.py')
    activate_this = (os.path.join(SCRIPTDIR, venv))
    # Python 3: exec(open(...).read()), Python 2: execfile(...)
    exec(open(activate_this).read(), dict(__file__=activate_this))

    # googleoauth.py requirement
    from oauth2client import file, client, tools
    from httplib2 import Http
    from apiclient.discovery import build