from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.generic import RedirectView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='about.jinja'), name="about"),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy-policy.jinja'), name="privacy"),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^$', RedirectView.as_view(url='/albums/'),
        name='home-page-redirect'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='gauth_logout'),
    url(r'^albums/', include('albums.urls', namespace='albums')),
    url(r'^labels/', include('classification.urls', namespace='labels')),
    url(r'^profile/', include('profiles.urls', namespace='profile')),
    url(r'^admin/', admin.site.urls),
]