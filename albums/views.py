from django.shortcuts import render


def index(request):
    context = {'message': 'Albums Index'}
    return render(request, 'albums/index.html', context)
