=====
Usage
=====

To use Django Outbox Middleware in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_outbox_middleware.apps.DjangoOutboxMiddlewareConfig',
        ...
    )

Add Django Outbox Middleware's URL patterns:

.. code-block:: python

    from django_outbox_middleware import urls as django_outbox_middleware_urls


    urlpatterns = [
        ...
        url(r'^', include(django_outbox_middleware_urls)),
        ...
    ]
