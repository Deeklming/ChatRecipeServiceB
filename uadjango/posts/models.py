from django.db import models
from datetime import datetime, timezone
from django.contrib.postgres.fields import ArrayField
from auths.models import Users

# Create your models here.
class Posts(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64, unique=True)
    images = models.JSONField(default=dict, null=True)
    content = models.TextField()
    amenity = ArrayField(models.CharField(max_length=64), null=True, default=list)
    price = models.DecimalField(max_digits=18, decimal_places=6)
    like_avg_score = models.FloatField(default=0.0)
    like_count = models.IntegerField(default=0)
    clip_count = models.IntegerField(default=0)
    available_start_at = models.DateTimeField(default=datetime.now(timezone.utc))
    available_end_at = models.DateTimeField(default=datetime.now(timezone.utc))
    position = models.CharField(max_length=64, null=True, default=None)
    hashtag = ArrayField(models.CharField(max_length=10), null=True, default=None)
    public = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title[:9]

class Comments(models.Model):
    post_id = models.ForeignKey("Posts", on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now(timezone.utc))
    public = models.BooleanField(default=True)
