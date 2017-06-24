from django.db import models
from albums.models import Genre, Album


class Location(models.Model):
    label = models.CharField(max_length=60, unique=True)

    def __repr__(self):
        return '<Location {0}>'.format(self.label)

    def __str__(self):
        return self.label


class GenreLabel(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    color_left = models.CharField(max_length=6)
    color_right = models.CharField(max_length=6)

    def __repr__(self):
        return '<GenreLabel {0}>'.format(self.genre.label)

    def __str__(self):
        return self.genre.label
