import os

from .base import *
if 'PORT' in os.environ:
    print "PORT environment variable found, assuming 12-factor/heroku."
    from .heroku import *
else:
    try:
        from .local import *
    except ImportError, exc:
        print "settings/local.py not found, assuming 12-factor/heroku."
        from .heroku import *
