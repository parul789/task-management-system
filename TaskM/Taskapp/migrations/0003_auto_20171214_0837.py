# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Taskapp', '0002_auto_20171212_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]