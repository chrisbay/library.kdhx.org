from albums.models import Album
from data.models import AlbumImport


def run():
    Album.objects.all().delete()
    AlbumImport.objects.all().delete()