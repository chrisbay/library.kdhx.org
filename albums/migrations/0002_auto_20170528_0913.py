# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-28 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediatype',
            name='label',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]