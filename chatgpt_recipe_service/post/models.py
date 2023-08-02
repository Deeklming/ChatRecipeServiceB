from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.contrib.auth import get_user_model


# User = get_user_model()

class Post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    body = models.TextField()
    # likes = models.ManyToManyField(User, related_name='like_post', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
