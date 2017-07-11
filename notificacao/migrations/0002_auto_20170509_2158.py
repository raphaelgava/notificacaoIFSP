# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 21:58
from __future__ import unicode_literals

from django.db import migrations

#python manage.py makemigrations --empty notificacao
def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Student'),
        Group(name=u'Employee'),
        Group(name=u'Professor'),
		Group(name=u'Admin'),
    ])
	
class Migration(migrations.Migration):

    dependencies = [
        ('notificacao', '0001_initial'),
    ]

    operations = [
		migrations.RunPython(apply_migration),
    ]
