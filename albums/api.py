import json
from django.core import serializers
from django.http import HttpResponse
from albums.models import Album


LABELS_TO_PRINT_KEY = 'labels_to_print'


def toggle_album_state(request, album_id=None, state=''):
    album = None
    user = request.user
    try:
        album_id = int(album_id)
        album = Album.objects.get(pk=album_id)
    except ValueError:
        album_id = None
    if album and user.is_authenticated() and request.method == 'POST':
        msg, action = {
            'star': lambda r, a: toggle_album_star(r, a),
            'print': lambda r, a: toggle_album_print(r, a)
        }[state](request, album)
        success = True
    else:
        success = False
        msg = "Invalid Request"
        action = ''
    return HttpResponse(
        json.dumps({"success": success, "msg": msg, "action": action}),
        content_type="application/json"
    )


def toggle_album_print(request, album):
    user = request.user
    if LABELS_TO_PRINT_KEY not in request.session or not request.session[LABELS_TO_PRINT_KEY]:
        request.session[LABELS_TO_PRINT_KEY] = []
    if album.id in request.session[LABELS_TO_PRINT_KEY]:
        request.session[LABELS_TO_PRINT_KEY].remove(album.id)
        msg = "{0} removed from print list".format(album.title)
        action = "removed"
    else:
        request.session[LABELS_TO_PRINT_KEY].append(album.id)
        msg = "{0} saved to print list".format(album.title)
        action = "saved"
    request.session.modified = True
    return (msg, action)


def toggle_album_star(request, album):
    user = request.user
    saved_albums = user.saved_albums.all()
    if album in saved_albums:
        user.saved_albums.remove(album)
        user.save()
        msg = "{0} removed from My Albums".format(album.title)
        action = "removed"
    else:
        user.saved_albums.add(album)
        user.save()
        msg = "{0} saved to My Albums".format(album.title)
        action = "saved"
    return (msg, action)


def labels_to_print(request):
    if LABELS_TO_PRINT_KEY in request.session:
        album_ids = request.session[LABELS_TO_PRINT_KEY]
        albums = Album.objects.filter(id__in=album_ids)
    else:
        albums = []
    return HttpResponse(
        serializers.serialize('json', list(albums), use_natural_foreign_keys=True),
        content_type="application/json"
    )
