import os
from urlparse import urlparse
from urllib import quote
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

SITE_SCHEME = urlparse(os.environ.get('SITE_URL', '')).scheme

def application(environ, start_response):
    # For some reason 'secure_scheme_headers' in gunicorn config
    # is failing us, so we'll do it manually here.
    if environ.get('HTTP_X_FORWARDED_PROTO') == 'https':
        environ['wsgi.url_scheme'] = 'https'

    # If the SITE_URL is explicitly defined, then we're going to
    # force a redirect to the proper protocol (http or https)
    # if necessary.
    if SITE_SCHEME and environ['wsgi.url_scheme'] != SITE_SCHEME:
        url = os.environ.get('SITE_URL')
        # http://www.python.org/dev/peps/pep-0333/#url-reconstruction
        url += quote(environ.get('SCRIPT_NAME', ''))
        url += quote(environ.get('PATH_INFO', ''))
        if environ.get('QUERY_STRING'):
            url += '?' + environ['QUERY_STRING']
        start_response("302 Found", [("Location", url)])
        return ["redirect to %s" % SITE_SCHEME]

    return django_app(environ, start_response)

# vim: ft=python
