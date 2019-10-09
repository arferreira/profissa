# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 14:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma', max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Informe um nome de usuário válido. Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .', 'invalid')], verbose_name='Apelido / Usuário'),
        ),
    ]