# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ")cf99-sxnt83rkdr1h^hm07$caas+ycom4s+iv#8b#=4u%3&bi"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_outbox_middleware",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'django_outbox_middleware.middleware.OutboxMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'django_outbox_middleware.middleware.OutboxMiddleware',
    )
