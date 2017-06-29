from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from albums.models import Album


class AlbumList(ListView):
    template_name = 'albums/album_list.jinja'
    paginate_by = 20
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Albums'
        return context


class AlbumDetail(DetailView):
    template_name = 'albums/album_detail.jinja'
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Album Detail'
        return context

    def get_object(self):
        return get_object_or_404(Album, id=int(self.args[0]))


class AlbumCreate(SuccessMessageMixin, CreateView):
    model = Album
    template_name = 'albums/album_form.jinja'
    fields = ['title', 'artist', 'label', 'media', 'genre', 'location']
    success_url = '/albums/'
    success_message = 'New album created: <strong>%(album)s</strong>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Album'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           album=self.object)
