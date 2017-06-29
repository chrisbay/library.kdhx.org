from django.conf.urls import url
from . import views

app_name = 'albums'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.AlbumCreate.as_view(), name='new-album'),
]