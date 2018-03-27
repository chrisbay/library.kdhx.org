from django.db import models


class ImportRecord(models.Model):
    orig_id = models.IntegerField()
    new_id = models.IntegerField()

    class Meta:
        abstract = True


class GenreLabelImport(ImportRecord):
    pass


class GenreImport(ImportRecord):
    pass


class AlbumImport(ImportRecord):
    pass
