from django.conf.urls import url, include
from . import views

app_name = 'labels'

urlpatterns = [
    url(r'^print$', views.print_labels, name='print-labels'),
]