from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render
from albums.models import MediaType


def index(request):
    return render(request, 'albums/index.html', {'page_title': 'Albums'})


def new(request):
    return render(request, 'albums/new.html', {'page_title': 'New Album'})


class MediaTypeCreate(CreateView):
    model = MediaType
    fields = ['label']
    success_url = '/albums/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Media Type'
        return context