from django.conf.urls import url
from . import views
from . import api

app_name = 'albums'

urlpatterns = [
    url(r'^$', views.AlbumList.as_view(), name='album-list'),
    url(r'^detail/([-\w]+)$', views.AlbumDetail.as_view(), name='album-detail'),
    url(r'^new/$', views.AlbumCreate.as_view(), name='album-new'),
    url(r'^edit/(?P<pk>[-\w]+)$', views.AlbumUpdate.as_view(), name='album-edit'),
    url(r'^star/(?P<album_id>[\d]+)$', api.toggle_album_star, name='star-album'),
    url(r'^label/([-\w]+)$', views.AlbumsByLabel.as_view(), name='albums-by-label'),
]