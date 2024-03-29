# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-01 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20180218_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='first',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='Artist First'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='last',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='Artist Last'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Artist Name'),
        ),
    ]
