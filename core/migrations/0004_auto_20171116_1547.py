# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20171116_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='provider',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='Profissional'),
        ),
    ]