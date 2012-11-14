import os
#import site

os.environ.setdefault('CELERY_LOADER', 'django')
# NOTE: you can also set DJANGO_SETTINGS_MODULE in your environment to override
# the default value in manage.py

# Add the app dir to the python path so we can import manage.
#wsgidir = os.path.dirname(__file__)
#site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

# manage adds /apps, /lib, and /vendor to the Python path.
import manage

import django.core.handlers.wsgi
django_app = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    # For some reason 'secure_scheme_headers' in gunicorn config
    # is failing us, so we'll do it manually here.
    if environ.get('HTTP_X_FORWARDED_PROTO') == 'https':
        environ['wsgi.url_scheme'] = 'https'
    return django_app(environ, start_response)

# vim: ft=python
