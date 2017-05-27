from django.conf.urls import url
from . import views

app_name = 'albums'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^media/new/$', views.new_media, name='new_media'),
]