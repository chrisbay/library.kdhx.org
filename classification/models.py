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


class LibraryAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __repr__(self):
        return '<LibraryAlbum {0} ({1})>'.format(self.album, self.location)

    def __str__(self):
        return '{0} ({1})'.format(self.album, self.location)
