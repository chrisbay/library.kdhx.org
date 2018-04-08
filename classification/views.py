from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from albums.api import LABELS_TO_PRINT_KEY


def print_labels(request):
    if LABELS_TO_PRINT_KEY in request.session:
        album_count = len(request.session['labels_to_print'])
    else:
        album_count = 0
    args = {
        'page_title': 'Print Labels',
        'album_count': album_count,
    }
    return render(request, 'classification/print_labels.jinja', args)


def reset_labels(request):
    del(request.session[LABELS_TO_PRINT_KEY])
    messages.add_message(request, messages.SUCCESS, 'All labels have been cleared')
    return redirect('albums:album-list')
