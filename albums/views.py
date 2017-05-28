from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib import messages
from albums.models import MediaType


def index(request):
    return render(request, 'albums/index.html', {'page_title': 'Albums'})


def new(request):
    return render(request, 'albums/new.html', {'page_title': 'New Album'})


class MediaTypeCreate(SuccessMessageMixin, CreateView):
    model = MediaType
    fields = ['label']
    success_url = '/albums/'
    success_message = 'New Media Type <strong>%(type_label)s</strong> created'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Media Type'
        return context

    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, 
            type_label=self.object.label)