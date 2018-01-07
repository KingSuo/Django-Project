# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 16:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_sendTime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='最近一次发送邮件时间'),
        ),
    ]
