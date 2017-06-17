from django.db import models


class MediaType(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __repr__(self):
        return self.label

    def __str__(self):
        return self.label
