from albums.models import Album, RecordLabel, Artist
from data.models import AlbumImport


def run():
    Album.objects.all().delete()
    RecordLabel.objects.all().delete()
    Artist.objects.all().delete()
    AlbumImport.objects.all().delete()
    RecordLabel.objects.create(name="Self")
    Artist.objects.create(name="Various Artists")