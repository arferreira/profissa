# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 17:45
from __future__ import unicode_literals

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20171116_1439'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]