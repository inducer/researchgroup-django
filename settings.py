# Django settings for scg project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

ADMINS = (
    ('Andreas Kloeckner', 'kloeckner@dam.brown.edu')
)

MANAGERS = ADMINS

import os
import os.path
SCG_BASE_DAM = '/webapp/scicomp/scg'

DEPLOYED = os.path.isdir(SCG_BASE_DAM)
if DEPLOYED:
    SCG_BASE = SCG_BASE_DAM
else:
    SCG_BASE = '/home/andreas/django/scg'

DATABASES = {
    'default': {
        'NAME': 'scicomp',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'scicomp',
        'PASSWORD': 'CHANGEME',
    }
}

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SCG_BASE,"../scg-media")

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/scicomp/media/'

STATIC_URL = "/scicomp/django-static/"
STATIC_ROOT = "/webapp/scicomp/scg-static"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3m2-z86@ybu1wa=7_)-k0a4arde6)ep+!g(i3rk_(%67&r6&e1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.app_directories.load_template_source',
    #'django.template.loaders.eggs.load_template_source',
)

if 0:
	MIDDLEWARE_CLASSES = (
	    'django.middleware.common.CommonMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.middleware.doc.XViewMiddleware',
	)

ROOT_URLCONF = 'scg.urls'

TEMPLATE_DIRS = (
    os.path.join(SCG_BASE, 'templates'),
    os.path.join(SCG_BASE, 'researchgroup/templates'),
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.sites',
    'scg.researchgroup',
    'django.contrib.admin',
    'django.contrib.staticfiles',
)

def PATH_GETTER(environ):
    path = environ["PATH_INFO"]
    while path.startswith("/"):
        path = path[1:]
    #assert path.startswith(SCG_BASE+"/")
    path = DYNSITE_ROOT+path
    return path

# Root URL of the Django site. Include trailing slash.
if DEPLOYED:
    DYNSITE_ROOT = '/scicomp/'
    #DYNSITE_ROOT = '/scicomp/go.fcgi/'
    STATICSITE_ROOT = '/scicomp/static/'
else:
    DYNSITE_ROOT = '/'
    STATICSITE_ROOT = '/static/'
