import json
from django.http import HttpResponse
from albums.models import Album


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
    return HttpResponse(
        json.dumps({"success": success, "msg": msg, "action": action}),
        content_type="application/json"
    )


def toggle_album_print(request, album):
    user = request.user
    key = 'labels_to_print'
    if key not in request.session:
        request.session[key] = []
    to_print = request.session[key]
    if album.id in to_print:
        to_print.remove(album.id)
        msg = "{0} removed from print list".format(album.title)
        action = "removed"
    else:
        to_print.append(album.id)
        msg = "{0} saved to print list".format(album.title)
        action = "saved"
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
