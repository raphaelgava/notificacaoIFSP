# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 19:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificacao', '0016_auto_20160901_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 7 characters.', max_length=7, unique=True, validators=[django.core.validators.RegexValidator('^[\\w]+$', 'Enter a valid username. This value may contain only letters, numbers characters.')], verbose_name='username'),
        ),
    ]
