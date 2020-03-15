from django.db import models
from django.contrib.auth.models import User

class Summary(models.Model):
    '''Model for user submitted 'tl;dr' or article summary'''

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # article_id = 
    # summary_text = 
    # created_on = 