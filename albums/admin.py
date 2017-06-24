from django.contrib import admin
from albums.models import *

admin.site.register(MediaType)
admin.site.register(RecordLabel)
admin.site.register(Artist)
admin.site.register(Location)
admin.site.register(Album)
