from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^$', RedirectView.as_view(url='/albums/'),
        name='home-page-redirect'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='gauth_logout'),
    url(r'^albums/', include('albums.urls', namespace='albums')),
    url(r'^profile/', include('profiles.urls', namespace='profile')),
    url(r'^admin/', admin.site.urls),
]