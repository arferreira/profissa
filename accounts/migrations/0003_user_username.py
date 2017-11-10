# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-10 00:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171109_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Informe um nome de usuário válido. Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .', 'invalid')], verbose_name='Apelido / Usuário'),
            preserve_default=False,
        ),
    ]