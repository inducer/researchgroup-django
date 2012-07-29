from django.conf.urls.defaults import *
from scg.researchgroup.models import *
import os
from django.conf import settings
import re

from django.contrib import admin
admin.autodiscover()

def get_patterns():
    urlb = "^"

    plist = [
            (urlb+r'/?$', 'scg.researchgroup.views.main_page'),

            (urlb+r'people/(?P<person_cat>[a-z]+)/$', 
                'scg.researchgroup.views.people'),

            (urlb+r'seminars/current/$', 
                'scg.researchgroup.views.current_seminars'),
            (urlb+r'seminars/by-year/(?P<year>[0-9]+)/$', 
                'scg.researchgroup.views.seminars'),
            (urlb+r'seminars/(?P<id>[0-9]+)/$', 
                'scg.researchgroup.views.seminar'),

            (urlb+r'reports/current/$', 
                'scg.researchgroup.views.current_reports'),
            (urlb+r'reports/by-year/(?P<year>[a-z0-9]+)/$', 
                'scg.researchgroup.views.reports'),
            (urlb+r'reports/(?P<year>[0-9]+)-(?P<number>[0-9]+)/$', 
                'scg.researchgroup.views.report'),

            (urlb+r'classes/$', 
                'scg.researchgroup.views.classes'),

            (urlb+r'news/(?P<id>[0-9]+)/$', 
                'scg.researchgroup.views.news_detail'),
            (urlb+r'news/$', 
                'scg.researchgroup.views.news'),

            (urlb+r'page/(?P<address>[a-zA-Z0-9/]*[a-zA-Z0-9])/$', 
                'scg.researchgroup.views.page'),

            (urlb+r'admin/', include(admin.site.urls)),
            ]
    if not settings.DEPLOYED:
        plist.extend([
            (r'static/(.*)$', 
            'django.views.static.serve', 
            {'document_root': os.path.join(settings.SCG_BASE, '..', 'static')}),
            (r'media/(.*)$', 
            'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
            ])
    return plist

urlpatterns = patterns('', *get_patterns())
handler404 = 'scg.researchgroup.views.handler404'
