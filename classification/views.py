from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from albums.models import Album
from classification.models import GenreLabel


def print_labels(request):
    if 'labels_to_print' in request.session:
        album_ids = request.session['labels_to_print']
        albums = Album.objects.filter(id__in=album_ids)
    else:
        albums = []
    args = {
        'page_title': 'Print Labels',
        'albums': albums,
    }
    return render(request, 'classification/print_labels.jinja', args)


def reset_labels(request):
    del(request.session['labels_to_print'])
    messages.add_message(request, messages.SUCCESS, 'All labels have been cleared')
    return redirect('albums:album-list')
