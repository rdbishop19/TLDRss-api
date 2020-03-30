from django.db import models
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from .summary import Summary


class SummaryUpvote(models.Model):
    ''' Model for User-submitted summary upvotes'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="summary_upvotes")
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, related_name="upvotes")

    class Meta:
        verbose_name = ("summaryupvote")
        verbose_name_plural = ("summaryupvote")
        unique_together = ['user', 'summary']

    # def __str__(self):
    #     return self.name

    def get_absolute_url(self):
        return reverse("summaryupvote_detail", kwargs={"pk": self.pk})
