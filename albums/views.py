from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib import messages
from albums.models import Album


class IndexView(ListView):
    template_name = 'albums/album_list.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Albums'
        return context

    def get_queryset(self):
        return Album.objects.all()


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
