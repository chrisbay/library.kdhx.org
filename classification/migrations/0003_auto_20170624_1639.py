# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-24 21:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0002_libraryalbum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libraryalbum',
            name='album',
        ),
        migrations.RemoveField(
            model_name='libraryalbum',
            name='location',
        ),
        migrations.DeleteModel(
            name='LibraryAlbum',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]