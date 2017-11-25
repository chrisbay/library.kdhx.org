from django.conf.urls import url, include
from . import views
from . import api

app_name = 'albums'

urlpatterns = [
    url(r'^$', views.AlbumList.as_view(), name='album-list'),
    url(r'^recent/([\d]+)$', views.RecentAlbumsList.as_view(), name='album-list-recent'),
    url(r'^detail/([-\w]+)$', views.AlbumDetail.as_view(), name='album-detail'),
    url(r'^new/$', views.AlbumCreate.as_view(), name='album-new'),
    url(r'^edit/(?P<pk>[-\w]+)$', views.AlbumUpdate.as_view(), name='album-edit'),
    url(r'^toggle/(?P<state>[\w]+)/(?P<album_id>[\d]+)$', api.toggle_album_state, name='toggle-album-state'),
    url(r'^label/([-\w]+)$', views.AlbumsByLabel.as_view(), name='albums-by-label'),
    url(r'^artist/([-\w]+)$', views.AlbumsByArtist.as_view(), name='albums-by-artist'),
    url(r'^genre/([-\w]+)$', views.AlbumsByGenre.as_view(), name='albums-by-genre'),
    url(r'^search/', views.AlbumSearch.as_view(), name='album-search'),
    url(r'^weekly-email$', views.weekly_email, name='weekly-email'),
]
