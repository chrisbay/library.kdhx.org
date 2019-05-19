from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from jinja2 import Environment
from albums.models import Album, Artist, RecordLabel


def get_spotify_search_url(term):
    return 'https://open.spotify.com/search/results/'+term

def get_entity_url(watson_obj):
    content_type = ContentType.objects.get(app_label=watson_obj.content_type.app_label,
                                           model=watson_obj.content_type.model)
    obj_class = content_type.model_class()
    url = ''
    if obj_class == Album:
        url = reverse('albums:album-detail', args=[watson_obj.object_id_int])
    elif obj_class == Artist:
        url = reverse('albums:albums-by-artist', args=[watson_obj.object_id_int])
    elif obj_class == RecordLabel:
        url = reverse('albums:albums-by-label', args=[watson_obj.object_id_int])
    return url

ENTITY_LABELS = {
    Album: 'Album',
    RecordLabel: 'Label',
    Artist: 'Artist',
}

def get_entity_type_label(watson_obj):
    content_type = ContentType.objects.get(app_label=watson_obj.content_type.app_label,
                                           model=watson_obj.content_type.model)
    obj_class = content_type.model_class()
    return ENTITY_LABELS[obj_class]

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_spotify_search_url': get_spotify_search_url,
        'get_entity_url': get_entity_url,
        'get_entity_type_label': get_entity_type_label,
    })
    return env
