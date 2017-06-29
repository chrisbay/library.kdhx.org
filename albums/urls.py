from django.conf.urls import url
from . import views

app_name = 'albums'

urlpatterns = [
    url(r'^$', views.AlbumList.as_view(), name='album-list'),
    url(r'^detail/([-\w]+)$', views.AlbumDetail.as_view(), name='album-detail'),
    url(r'^new/$', views.AlbumCreate.as_view(), name='album-new'),
]