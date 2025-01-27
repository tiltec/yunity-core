"""wuppdays URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

import yunity.api.urls
import yunity.doc.flask_swagger

urlpatterns = [
    url(r'^api/', include(yunity.api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^doc$', yunity.doc.flask_swagger.doc),
]


# easy solution for serving a frontend from Django
# TODO: remove if superceded
if getattr(settings, 'LOCAL_WEBAPP_PATH', None):
    urlpatterns += [
        url('^$', 'django.views.static.serve', {
            'path': 'index.html',
            'document_root': settings.LOCAL_WEBAPP_PATH,
            'show_indexes': True,
        }),
        url('^(?P<path>.*)', 'django.views.static.serve', {
            'document_root': settings.LOCAL_WEBAPP_PATH,
            'show_indexes': True,
        })
    ]
