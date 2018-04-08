from haystack import indexes

from albums.models import Album


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Album
