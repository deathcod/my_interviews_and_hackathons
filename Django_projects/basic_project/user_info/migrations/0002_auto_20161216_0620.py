# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-16 06:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='Date_of_birth',
            new_name='dob',
        ),
    ]