# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-26 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genrelabel',
            name='genre',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='albums.Genre'),
        ),
    ]
