from django.db import models

class Feed(models.Model):
    '''Feed model'''

    name = models.CharField(max_length=255)
    feed_url = models.URLField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)