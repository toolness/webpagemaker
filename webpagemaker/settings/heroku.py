# This is an example settings/local.py file.
# These settings overrides what's in settings/base.py

# To extend any settings from settings/base.py here's an example:
#from . import base
#INSTALLED_APPS = base.INSTALLED_APPS + ['debug_toolbar']

import os
import dj_database_url

from .base import INSTALLED_APPS

INSTALLED_APPS.extend(['gunicorn'])

DATABASES = {
    'default': dj_database_url.config(),
}

SESSION_COOKIE_SECURE = True

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = ('DEBUG' in os.environ)

# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = ('DEV' in os.environ)

# Make this unique, and don't share it with anybody.  It cannot be blank.
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Default filesystem cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.environ.get('CACHE_LOCATION', 'brian-is-clever')
    }
}

# Uncomment and replace this as necessary!
SITE_URL = os.environ.get('SITE_URL',
                          'http://localhost:%s' % os.environ['PORT'])

if 'CLOPENBADGER_URL' in os.environ:
    CLOPENBADGER_URL = os.environ('CLOPENBADGER_URL')

if 'CLOPENBADGER_SECRET' in os.environ:
    CLOPENBADGER_SECRET = os.environ('CLOPENBADGER_SECRET')
