# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutboxRequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('request_uuid', models.UUIDField()),
                ('request_path', models.TextField()),
                ('request_body', models.TextField(blank=True, null=True)),
                ('response_status_code', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
