import uuid

from django.test import TestCase, Client, override_settings

from django_outbox_middleware.models import OutboxRequestLog


class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_echo_works(self):
        resp = self.client.post('/echo/', 'ping', content_type='text/plain')
        self.assertEqual(resp.content, b'ping')

    def test_no_header_set_no_log_created(self):
        self.client.post('/echo/', 'ping', content_type='text/plain')

        self.assertEqual(OutboxRequestLog.objects.count(), 0)

    def test_log_created_if_outbox_header_set(self):
        uuid_str = str(uuid.uuid4())
        self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        self.assertEqual(OutboxRequestLog.objects.count(), 1)
        
        log = OutboxRequestLog.objects.get()
        self.assertEqual(str(log.request_uuid), uuid_str)
        self.assertEqual(log.request_path, '/echo/')
        self.assertEqual(log.request_body, None)
        self.assertEqual(log.response_status_code, 200)

    def test_middleware_intercepts_second_request_with_identical_id(self):
        uuid_str = str(uuid.uuid4())
        resp1 = self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        self.assertEqual(resp1.content, b'ping')

        resp2 = self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        self.assertEqual(resp2.content, b'OK')
        self.assertEqual(resp2.status_code, 202)


        is_flagged_list = list(OutboxRequestLog.objects.values_list(
            'request_flagged_duplicate', flat=True
        ))

        self.assertEqual(OutboxRequestLog.objects.count(), 2)
        self.assertEqual(is_flagged_list, [False, True])

    def test_requests_that_error_arent_interecepted_2nd_time(self):
        uuid_str = str(uuid.uuid4())
        resp1 = self.client.post(
            '/asdasdasdasd/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        self.assertEqual(resp1.status_code, 404)

        resp2 = self.client.post(
            '/asdasdasdasd/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=uuid_str,
        )

        self.assertEqual(resp2.status_code, 404)

        is_flagged_list = list(OutboxRequestLog.objects.values_list(
            'request_flagged_duplicate', flat=True
        ))

        self.assertEqual(OutboxRequestLog.objects.count(), 2)
        self.assertEqual(is_flagged_list, [False, False])

    def test_requests_with_different_uuids_arent_flagged(self):
        self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=str(uuid.uuid4()),
        )
        self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=str(uuid.uuid4()),
        )

        is_flagged_list = list(OutboxRequestLog.objects.values_list(
            'request_flagged_duplicate', flat=True
        ))
        self.assertEqual(is_flagged_list, [False, False])

    @override_settings(OUTBOX_LOG_BODY=True)
    def test_body_logged_when_enabled(self):
        self.client.post(
            '/echo/',
            'ping',
            content_type='text/plain',
            HTTP_OUTBOX_REQUEST_UUID=str(uuid.uuid4()),
        )

        log = OutboxRequestLog.objects.get()
        self.assertEqual(log.request_body, 'ping')
