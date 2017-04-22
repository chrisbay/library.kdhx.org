from django.shortcuts import render


def index(request):
    context = {'message': 'KDHX Music Library'}
    return render(request, 'albums/index.html', context)
