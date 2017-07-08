from django.db import models
from django.contrib.auth.models import AbstractUser
from albums.models import Album


class LibraryUser(AbstractUser):
    saved_albums = models.ManyToManyField(Album)
