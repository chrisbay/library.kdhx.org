import json
from django.http import HttpResponse
from albums.models import Album


def toggle_album_star(request, album_id=None):
    album = None
    user = request.user
    try:
        album_id = int(album_id)
        album = Album.objects.get(pk=album_id)
    except ValueError:
        album_id = None
    if album and user.is_authenticated() and request.method == 'POST':
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
        success = True
    else:
        success = False
        msg = "Invalid Request"
    return HttpResponse(
        json.dumps({"success": success, "msg": msg, "action": action}),
        content_type="application/json"
    )
