from django.db import models

# Create your models here.
class Hashtags(models.Model):
    theme = models.CharField(max_length=18)
    tag = models.CharField(max_length=30)
    note = models.CharField(max_length=100, null=True, default=None)
    
    def __str__(self) -> str:
        return self.tag
