from . import git

from django.conf.urls.defaults import patterns, include

def throw(request):
    """
    Throw an exception so that the user can see all of Django's
    debugging information.
    """

    i_am_not_defined

urlpatterns = patterns('',
    (r'^throw$', throw),
    (r'^git-pull$', git.pull),
)
