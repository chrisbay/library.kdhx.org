from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from albums.models import Album, Artist, RecordLabel

DEFAULT_MEDIA_ID = 1
DEFAULT_GENRE_ID = 42
DEFAULT_LOCATION_ID = 2


class AlbumCreateForm(forms.ModelForm):
    new_artist_first = forms.CharField(required=False, label="Artist First")
    new_artist_last = forms.CharField(required=False, label="Artist Last")
    new_artist_name = forms.CharField(required=False, label="Artist Name")
    new_label = forms.CharField(required=False, label="New Record Label")

    class Meta:
        model = Album
        fields = ['title', 'artist', 'new_artist_first', 'new_artist_last',
                  'new_artist_name', 'labels', 'new_label', 'media', 'genre',
                  'location']
        widgets = {
            'artist': autocomplete.ModelSelect2(url='/albums/artist-autocomplete/'),
            'labels': autocomplete.ModelSelect2Multiple(url='/albums/labels-autocomplete/')
        }

    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['artist'].required = False
        self.fields['labels'].required = False
        self.fields['media'].initial = DEFAULT_MEDIA_ID
        self.fields['genre'].initial = DEFAULT_GENRE_ID
        self.fields['location'].initial = DEFAULT_LOCATION_ID

    @staticmethod
    def has_new_artist(data):
        return ((data['new_artist_first'] and
                data['new_artist_last']) or
                data['new_artist_name'])

    def clean(self):
        super(AlbumCreateForm, self).clean()
        album_data = self.cleaned_data
        if not album_data['artist'] and not self.has_new_artist(album_data):
            raise ValidationError(('Artist not specified, or info missing. '
                                   'If creating a new artist, '
                                   'provide both Artist First and Artist last,'
                                   ' or Artist Name.'))
        if not album_data['labels'] and not album_data['new_label']:
            raise ValidationError('No label(s) specified')

    def save(self, commit=True):
        album = super(AlbumCreateForm, self).save(commit=False)
        album_data = self.cleaned_data
        if self.has_new_artist(album_data):
            kwargs = {'first': album_data['new_artist_first'],
                      'last': album_data['new_artist_last'],
                      'name': album_data['new_artist_name']}
            new_artist = Artist.create(**kwargs)
            new_artist.save()
            album.artist = new_artist
        # need to save before potentially modifying the labels QuerySet
        album.save()
        self.save_m2m()
        if album_data['new_label']:
            new_label = RecordLabel(name=album_data['new_label'])
            new_label.save()
            album.labels.clear()
            album.labels.add(new_label)
        return album


class AlbumSearchForm(SearchForm):

    def search(self):
        sqs = SearchQuerySet()
        term = self.cleaned_data['q']
        if term == '':
            sqs = sqs.all()
        else:
            sqs = sqs.filter(content__contains=term)
        return sqs


class ArtistUpdateForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ['first', 'last', 'name']

    def clean(self):
        super(ArtistUpdateForm, self).clean()
        artist_data = self.cleaned_data

        if artist_data['name'] and (artist_data['first'] or artist_data['last']):
            raise ValidationError(('First or Last fields may not be specified '
                                   'if specifying Name field'))

        if not artist_data['name'] and not (artist_data['first'] and artist_data['last']):
            raise ValidationError(('Must specify both First and Last, or Name. '
                                   'If creating an artist with no last name '
                                   '(e.g. Madonna) then use the Name field.'))