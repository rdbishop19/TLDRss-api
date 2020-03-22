from django.db import models
from django.contrib.auth.models import User

from .feed import Feed

class FeedSubscription(models.Model):
    '''Model for user-subscribed feed sources'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ["user", "feed"]