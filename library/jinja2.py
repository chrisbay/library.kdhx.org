from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment


def get_spotify_search_url(term):
    return 'https://open.spotify.com/search/results/'+term


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_spotify_search_url': get_spotify_search_url
    })
    return env
