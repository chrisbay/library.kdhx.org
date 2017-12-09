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

    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['artist'].required = False
        self.fields['labels'].required = False
        self.fields['media'].initial = DEFAULT_MEDIA_ID
        self.fields['genre'].initial = DEFAULT_GENRE_ID
        self.fields['location'].initial = DEFAULT_LOCATION_ID

    def clean(self):
        super(AlbumCreateForm, self).clean()
        album = self.cleaned_data
        new_artist_fields_present = ((album['new_artist_first'] and
                                     album['new_artist_last']) or
                                     album['new_artist_name'])
        if not album['artist'] and not new_artist_fields_present:
            raise ValidationError(('Artist not specified, or info missing. '
                                   'If creating a new artist, '
                                   'provide both Artist First and Artist last,'
                                   ' or Artist Name.'))
        if album['artist'] and new_artist_fields_present:
            raise ValidationError(('Both existing and new artist specified.'
                                   'To assign a new artist, clear the '
                                   'Artist field'))
        if not album['labels'] and not album['new_label']:
            raise ValidationError('No label(s) specified')

    def save(self, commit=True):
        album = super(AlbumCreateForm, self).save(commit=False)
        album_data = self.cleaned_data
        if not album_data['artist']:
            kwargs = {'first': album_data['new_artist_first'],
                      'last': album_data['new_artist_last'],
                      'name': album_data['new_artist_name']}
            new_artist = Artist.create(**kwargs)
            new_artist.save()
            album.artist = new_artist
        # need to save before potentially modifying the labels QuerySet
        album.save()
        self.save_m2m()
        print(album.labels)
        if not album_data['labels']:
            new_label = RecordLabel(name=album_data['new_label'])
            new_label.save()
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

