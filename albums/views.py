import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from haystack.generic_views import SearchView
from reversion.views import RevisionMixin
from dal import autocomplete

from albums.forms import AlbumCreateForm, AlbumSearchForm
from albums.models import Album, RecordLabel, Artist, Genre

PAGE_SIZE = 30


class ContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title
        context['user'] = self.request.user
        return context


class UserContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_albums'] = self.request.user.saved_albums.all()
        return context


class AlbumList(UserContextMixin, ListView):
    title = 'Albums'
    template_name = 'albums/album_list.jinja'
    paginate_by = PAGE_SIZE
    model = Album


class RecentAlbumsList(AlbumList):
    title = 'Albums Added In The Past {days} Days'
    paginate_by = None
    
    def dispatch(self, request, *args, **kwargs):
        self.days = int(self.args[0])
        if self.days < 1:
            return redirect('albums:album-list')
        else:
            return super(RecentAlbumsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        oldest_date = datetime.datetime.now() - datetime.timedelta(days=self.days)
        return Album.objects.filter(created__date__gt=oldest_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.title.format(days=self.days)
        context['page_title'] = title
        context['page_heading'] = title
        return context


class AlbumDetail(UserContextMixin, DetailView):
    title = 'Album Detail'
    template_name = 'albums/album_detail.jinja'
    model = Album
    context_object_name = 'album'

    def get_object(self):
        return get_object_or_404(Album, id=int(self.args[0]))


class AlbumsByLabel(UserContextMixin, ListView):
    title = 'Albums on '
    template_name = 'albums/album_list.jinja'
    model = Album
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        label_id = self.args[0]
        label = RecordLabel.objects.get(id=label_id)
        self.label = label
        return label.album_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title + self.label.name
        context['page_heading'] = context['page_title']
        return context


class AlbumsByArtist(UserContextMixin, ListView):
    title = 'Albums by '
    template_name = 'albums/album_list.jinja'
    model = Album
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        artist_id = self.args[0]
        artist = Artist.objects.get(id=artist_id)
        self.artist = artist
        return artist.album_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title + self.artist.display_name
        context['page_heading'] = context['page_title']
        return context


class AlbumsByGenre(UserContextMixin, ListView):
    title = 'Albums by Genre'
    template_name = 'albums/album_list.jinja'
    model = Album
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        genre_id = self.args[0]
        genre = Genre.objects.get(id=genre_id)
        self.genre = genre
        return genre.album_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.genre.label + ' Albums'
        context['page_heading'] = context['page_title']
        return context


class AlbumSearch(UserContextMixin, SearchView):
    title = 'Album Search'
    template_name = 'albums/album_search.jinja'
    form_class = AlbumSearchForm
    paginate_by = PAGE_SIZE


class AlbumCreate(PermissionRequiredMixin, ContextMixin, RevisionMixin,
                  SuccessMessageMixin, CreateView):
    title = 'New Album'
    permission_required = 'albums.add_album'
    model = Album
    template_name = 'albums/album_form.jinja'
    form_class = AlbumCreateForm
    success_url = '/albums/'
    success_message = 'New album created: <strong>%(album)s</strong>'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           album=self.object)


class AlbumUpdate(PermissionRequiredMixin, ContextMixin, RevisionMixin,
                  SuccessMessageMixin, UpdateView):
    title = 'Edit Album'
    permission_required = 'albums.change_album'
    model = Album
    template_name = 'albums/album_form.jinja'
    form_class = AlbumCreateForm
    success_url = '/albums/'
    success_message = 'Album updated: <strong>%(album)s</strong>'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           album=self.object)


def weekly_email(request):
    start_date = datetime.date.today()
    end_date = start_date - datetime.timedelta(days=7)
    albums = list(Album.objects.filter(created__date__gt=end_date))
    args = {
        'albums': sorted(albums, key=lambda x: (x.genre.label, x.artist.display_name)),
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'albums/weekly_email.jinja', args)


class ArtistAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Artist.objects.none()
        qs = Artist.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class LabelsAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return RecordLabel.objects.none()
        qs = RecordLabel.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs