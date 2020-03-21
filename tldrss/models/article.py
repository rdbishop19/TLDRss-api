from django.db import models
from .feed import Feed

class Article(models.Model):
    '''Article class'''

    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    pub_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)