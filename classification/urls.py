from django.conf.urls import url, include
from . import views

app_name = 'labels'

urlpatterns = [
    url(r'^print$', views.print_labels, name='print-labels'),
    url(r'^print-reset$', views.reset_labels, name='reset-print-labels'),
]
