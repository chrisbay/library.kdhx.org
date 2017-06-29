from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib import messages
from albums.models import Album


def index(request):
    return render(request, 'albums/index.jinja', {'page_title': 'Albums'})


def new(request):
    return render(request, 'albums/new.jinja', {'page_title': 'New Album'})


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
