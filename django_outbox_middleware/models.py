# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel


class OutboxRequestLog(TimeStampedModel):
    request_uuid = models.UUIDField()
    response_status_code = models.IntegerField()
