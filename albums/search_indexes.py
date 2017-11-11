import datetime
from haystack import indexes
from albums.models import Album


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(document=True, use_template=True)
    artist = indexes.CharField(model_attr='artist')

    def get_model(self):
        return Album
