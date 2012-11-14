# This is an example settings/local.py file.
# These settings overrides what's in settings/base.py

# To extend any settings from settings/base.py here's an example:
#from . import base
#INSTALLED_APPS = base.INSTALLED_APPS + ['debug_toolbar']

import os
import dj_database_url

from .base import INSTALLED_APPS

def configure_database_url():
    """
    If DATABASE_URL isn't in the environment, see if anything that
    ends with DATABASE_URL is. If there is, set DATABASE_URL to its
    value. This allows for seamless integration with e.g.
    cleardb, which sets the CLEARDB_DATABASE_URL variable.
    """
    
    if 'DATABASE_URL' not in os.environ:
        print "DATABASE_URL not found in environment."
        candidates = [name for name in os.environ
                      if name.endswith('DATABASE_URL')]
        if len(candidates) == 1:
            print "Using %s instead." % candidates[0]
            os.environ['DATABASE_URL'] = os.environ[candidates[0]]

configure_database_url()

INSTALLED_APPS.extend(['gunicorn'])

DATABASES = {
    # Pull from the DATABASE_URL environment variable.
    'default': dj_database_url.config(),
}

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = ('DEBUG' in os.environ)

SESSION_COOKIE_SECURE = ('SESSION_COOKIE_SECURE' in os.environ)

# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = ('DEV' in os.environ)

# We need to always be able to serve static files when deploying to Heroku.
SERVE_STATIC_FILES = True

# Make this unique, and don't share it with anybody.  It cannot be blank.
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Default filesystem cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.environ.get('CACHE_LOCATION', 'brian-is-clever')
    }
}

if 'SITE_URL' in os.environ or 'PORT' in os.environ:
    SITE_URL = os.environ.get('SITE_URL',
                              'http://localhost:%s' % 
                              os.environ.get('PORT', ''))

if 'CLOPENBADGER_URL' in os.environ:
    CLOPENBADGER_URL = os.environ('CLOPENBADGER_URL')

if 'CLOPENBADGER_SECRET' in os.environ:
    CLOPENBADGER_SECRET = os.environ('CLOPENBADGER_SECRET')
