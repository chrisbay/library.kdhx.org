from django import forms
from django.core.exceptions import ValidationError
from albums.models import Album, Artist, RecordLabel

DEFAULT_MEDIA_ID = 1
DEFAULT_GENRE_ID = 42
DEFAULT_LOCATION_ID = 2


class AlbumCreateForm(forms.ModelForm):
    new_artist = forms.CharField(required=False)
    new_label = forms.CharField(required=False)

    class Meta:
        model = Album
        fields = ['title', 'artist', 'new_artist', 'labels', 'new_label',
                  'media', 'genre', 'location']

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
        validation_errors = ""
        if not album['artist'] and not album['new_artist']:
            validation_errors = 'No artist specified'
        if not album['labels'] and not album['new_label']:
            validation_errors = 'No label(s) specified'
        if validation_errors:
            raise ValidationError(validation_errors)

    def save(self, commit=True):
        album = super(AlbumCreateForm, self).save(commit=False)
        album_data = self.cleaned_data
        if not album_data['artist']:
            new_artist = Artist(name=album_data['new_artist'])
            new_artist.save()
            album.artist = new_artist
        # need to save before potentially modifying the labels QuerySet
        album.save() 
        if not album_data['labels']:
            new_label = RecordLabel(name=album_data['new_label'])
            new_label.save()
            album.labels.add(new_label)
        return album
