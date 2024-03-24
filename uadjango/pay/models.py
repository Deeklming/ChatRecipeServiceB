from django.db import models
from datetime import datetime, timezone
from auths.models import Users
from posts.models import Posts

# Create your models here.
class Reservations(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=datetime.now(timezone.utc))
    head_count = models.IntegerField(default=0)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    payment_price = models.DecimalField(max_digits=18, decimal_places=6)

    def __str__(self) -> str:
        return self.id
