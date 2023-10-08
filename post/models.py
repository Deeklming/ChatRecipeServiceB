from django.db import models
from user.models import User

# Create your models here.
def post_like_who_json():
    return {'like_count':0}

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    status = models.BooleanField(default=True)
    like = models.JSONField(default=post_like_who_json)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Post:{self.id}.{self.user.nickname}.{self.body}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    status = models.BooleanField(default=True)
    reference_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='r_p')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment:{self.id}.{self.user.nickname}:{self.body}'
