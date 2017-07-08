from django.contrib import admin
from reversion.admin import VersionAdmin
from albums.models import *

admin.site.register(MediaType)
admin.site.register(RecordLabel)
admin.site.register(Artist)
admin.site.register(Location)


@admin.register(Album)
class AlbumAdmin(VersionAdmin):
    pass
