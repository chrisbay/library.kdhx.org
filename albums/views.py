from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib import messages
from albums.models import MediaType


def index(request):
    return render(request, 'albums/index.jinja', {'page_title': 'Albums'})
