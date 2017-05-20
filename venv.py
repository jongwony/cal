import os

# virtualenv
SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))

venv_name = '_ccal'
osdir = 'Scripts' if os.name is 'nt' else 'bin'
venv = os.path.join(venv_name, osdir, 'activate_this.py')
activate_this = (os.path.join(SCRIPTDIR, venv))
# Python 3: exec(open(...).read()), Python 2: execfile(...)
exec(open(activate_this).read(), dict(__file__=activate_this))