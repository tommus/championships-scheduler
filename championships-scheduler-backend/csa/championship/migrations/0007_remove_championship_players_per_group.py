# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 12:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('championship', '0006_auto_20161010_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='championship',
            name='players_per_group',
        ),
    ]
