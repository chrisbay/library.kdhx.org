from django.shortcuts import render


def index(request):
    context = {'message': 'Albums Index', 'page_title': 'Albums'}
    return render(request, 'albums/index.html', context)


def new(request):
    context = {'page_title': 'New Album'}
    return render(request, 'albums/new.html', context)