from django.shortcuts import render


def index(request):
    return render(request, 'albums/index.html', {'page_title': 'Albums'})


def new(request):
    return render(request, 'albums/new.html', {'page_title': 'New Album'})


def new_media(request):
    return render(request, 'albums/media/new.html', {'page_title': 'New Media Type'})