from django.conf.urls import url
from . import views

app_name = 'profile'

urlpatterns = [
    url(r'^starred/$', views.starred_albums, name='my-albums'),
]
