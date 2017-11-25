import datetime
from django.shortcuts import render
from albums.models import Album


def print_labels(request):
    start_date = datetime.date.today()
    end_date = start_date - datetime.timedelta(days=30)
    albums = list(Album.objects.filter(created__date__gt=end_date))
    args = {
        'page_title': 'Print Labels',
        'albums': albums
    }
    return render(request, 'classification/print_labels.jinja', args)
