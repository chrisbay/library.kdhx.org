# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-24 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_auto_20170624_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='first',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='artist',
            name='last',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]
