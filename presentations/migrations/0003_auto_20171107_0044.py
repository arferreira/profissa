# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentations', '0002_lead_suggestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'verbose_name': 'Lead', 'verbose_name_plural': 'Leads'},
        ),
        migrations.AddField(
            model_name='lead',
            name='subscribe',
            field=models.BooleanField(choices=[(True, 'Contactado por email'), (False, 'Não contactado')], default=False, verbose_name='Contactado'),
        ),
    ]