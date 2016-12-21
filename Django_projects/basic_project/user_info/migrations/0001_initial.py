# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('age', models.CharField(max_length=3)),
                ('Date_of_birth', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
