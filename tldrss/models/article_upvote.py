from django.db import models
from django.contrib.auth.models import User
from .article import Article

class ArticleUpvote(models.Model):
    '''user-submitted article upvotes'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upvotes")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="upvotes")

    class Meta:
        unique_together = ['user', 'article']