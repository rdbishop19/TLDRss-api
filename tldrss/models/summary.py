from django.db import models
from django.contrib.auth.models import User
from .article import Article
class Summary(models.Model):
    '''Model for user submitted 'tl;dr' or article summary'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    summary_text = models.CharField(max_length=255, null=False)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    # edited_on = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    class Meta:
        # verbose_name = "summary"
        verbose_name_plural = "summaries"