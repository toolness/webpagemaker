from .base import *
try:
    from .local import *
except ImportError, exc:
    print "settings/local.py not found, assuming 12-factor/heroku."
    from .heroku import *
