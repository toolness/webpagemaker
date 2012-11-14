from django.conf import settings
from django.conf.urls.defaults import patterns, include

from . import api, browserid_ajax

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'webpagemaker.website.views.home'),
    (r'^projects$', 'webpagemaker.website.views.projects'),
    (r'^gallery$', 'webpagemaker.website.views.gallery'),
    (r'^about$', 'webpagemaker.website.views.about'),
    (r'^editor$', 'webpagemaker.editor.views.default_editor'),
    (r'^webarcade$', 'webpagemaker.website.views.webarcade'),
    (r'^content_guidelines$', 'webpagemaker.website.views.guidelines'),
    (r'^projects/(?P<name>[A-Za-z0-9\-_]+)$',
      'webpagemaker.learning_projects.views.render', {}, 'view_project'),
    (r'^projects/(?P<name>[A-Za-z0-9\-_]+)/edit$',
     'webpagemaker.editor.views.editor', {'remix': 'view_project'},
     'edit_project'),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
     {'url': '/media/img/favicon.ico'}),
    (r'', include(api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^browserid/', include(browserid_ajax.urls))
)

if not hasattr(settings, 'SERVE_STATIC_FILES'):
    settings.SERVE_STATIC_FILES = settings.DEBUG

# Potentially serve media files through Django.
#
# TODO: We probably shouldn't be using django.views.static here
# because the documentation constantly claims that it's probably
# insecure. However, its claim that static files served through
# Django are always grossly inefficient is not necessarily true, for
# the same reason that serving rendered templates through Django
# aren't grossly inefficient: if we front our app with a cache like
# Varnish and provide proper headers, we can easily ensure that our
# static files are served efficiently.
if settings.SERVE_STATIC_FILES:
    from django.views.static import serve as orig_static_serve

    def debug_static_serve(request, path, document_root):
        # Just like django.views.static.serve, but force the
        # removal of the X-Frame-Options header. This allows
        # our static files to be delivered the way they will
        # be in production, and also allows our browser unit tests
        # to use iframes.
        response = orig_static_serve(request, path, document_root)
        response.no_frame_options = True
        return response

    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, debug_static_serve,
         {'document_root': settings.MEDIA_ROOT}),
    )

    # Remove leading and trailing slashes so the regex matches.
    learning_static_url = settings.LEARNING_PROJECTS_STATIC_URL
    learning_static_url = learning_static_url.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % learning_static_url,
         debug_static_serve,
         {'document_root': settings.LEARNING_PROJECTS_STATIC_ROOT}),
    )

if settings.DEBUG:
    from . import debugging
    
    urlpatterns += debugging.urlpatterns

if settings.DEV:
    from .learning_projects import dropbox
    
    urlpatterns += dropbox.urlpatterns
