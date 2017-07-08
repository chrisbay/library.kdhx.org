from django.shortcuts import render
from django.http import HttpResponseRedirect
from profiles.models import LibraryUser


def starred_albums(request):
    if not request.user:
        return HttpResponseRedirect('/')
    albums = request.user.saved_albums.all()
    context = {'page_title': 'My Albums', 'album_list': albums}
    return render(request, 'profiles/starred.jinja', context)
