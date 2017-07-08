from django.db import models


class MediaType(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __repr__(self):
        return '<MediaType {0}>'.format(self.label)

    def __str__(self):
        return self.label


class RecordLabel(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __repr__(self):
        return '<RecordLabel {0}>'.format(self.name)

    def __str__(self):
        return self.name


class Artist(models.Model):
    first = models.CharField(max_length=64, blank=True, default='')
    last = models.CharField(max_length=64, blank=True, default='')
    name = models.CharField(max_length=128, blank=True, default='')

    @classmethod
    def create(cls, first=None, last=None, name=None):
        if not ((first and last) or name):
            raise ValueError('Artist requires both first and last, or name')
        return cls(first=first, last=last, name=name)

    @property
    def display_name(self):
        if not self.name:
            return '{0} {1}'.format(self.first, self.last)
        return self.name

    @property
    def file_under(self):
        if not self.name:
            return self.last[0].upper()
        elif self.name == 'Various Artists':
            return '#'
        return self.name[0].upper()

    def __repr__(self):
        return '<Artist {0}>'.format(self.display_name)

    def __str__(self):
        return self.display_name


class Genre(models.Model):
    label = models.CharField(max_length=60)

    def __repr__(self):
        return '<Genre {0}>'.format(self.label)

    def __str__(self):
        return self.label


class Location(models.Model):
    label = models.CharField(max_length=60, unique=True)

    def __repr__(self):
        return '<Location {0}>'.format(self.label)

    def __str__(self):
        return self.label


class Album(models.Model):
    title = models.CharField(max_length=256)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    labels = models.ManyToManyField(RecordLabel)
    media = models.ForeignKey(MediaType, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    @property
    def label_display_text(self):
        return ' / '.join([label.name for label in self.labels.all()])

    def __repr__(self):
        return '<Album {0} - {1}>'.format(self.artist.display_name, self.title)

    def __str__(self):
        return '{0} - {1}'.format(self.artist.display_name, self.title)
