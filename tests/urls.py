# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_outbox_middleware.urls import urlpatterns as django_outbox_middleware_urls

from . import views

urlpatterns = [
    url(r'^', include(django_outbox_middleware_urls, namespace='django_outbox_middleware')),
    url(r'^echo/$', views.EchoView.as_view()),
]
