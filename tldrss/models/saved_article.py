from django.db import models
from django.contrib.auth.models import User

from tldrss.models import Article

class SavedArticle(models.Model):
    '''Many to many user saved article relationship'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="user_saves")

    class Meta:
        unique_together = ['user', 'article']