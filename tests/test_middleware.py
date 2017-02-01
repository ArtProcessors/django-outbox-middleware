import uuid

from django.test import TestCase, Client

from django_outbox_middleware.models import OutboxRequestLog


class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_echo_works(self):
        resp = self.client.post('/echo/', 'ping', content_type='text/plain')
        assert resp.content == 'ping'

    def test_no_header_set_no_log_created(self):
        self.client.post('/echo/', 'ping', content_type='text/plain')

        assert OutboxRequestLog.objects.count() == 0


    def test_log_created_if_outbox_header_set(self):
        uuid_str = str(uuid.uuid4())
        self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        assert OutboxRequestLog.objects.count() == 1
        
        log = OutboxRequestLog.objects.get()
        self.assertEqual(str(log.request_uuid), uuid_str)
        assert log.request_path == '/echo/'
