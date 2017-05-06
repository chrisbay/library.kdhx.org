"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^$', TemplateView.as_view(template_name="login.html")),
    url(r'^logout/$', logout, {'next_page': '/'}, name='gauth_logout'),
    url(r'^login-error/$', TemplateView.as_view(template_name="login-error.html")),
    url(r'^albums/', include('albums.urls', namespace='albums')),
    url(r'^admin/', admin.site.urls),
]