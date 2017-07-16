from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from reversion.views import RevisionMixin
from albums.models import Album


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
    paginate_by = 20
    model = Album


class AlbumDetail(UserContextMixin, DetailView):
    title = 'Album Detail'
    template_name = 'albums/album_detail.jinja'
    model = Album
    context_object_name = 'album'

    def get_object(self):
        return get_object_or_404(Album, id=int(self.args[0]))


class AlbumCreate(PermissionRequiredMixin, ContextMixin, RevisionMixin,
                  SuccessMessageMixin, CreateView):
    title = 'New Album'
    permission_required = 'albums.add_album'
    model = Album
    template_name = 'albums/album_form.jinja'
    fields = ['title', 'artist', 'labels', 'media', 'genre', 'location']
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
    fields = ['title', 'artist', 'labels', 'media', 'genre', 'location']
    success_url = '/albums/'
    success_message = 'Album updated: <strong>%(album)s</strong>'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           album=self.object)
