from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname=None):
        use_in_migrations = True

        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')

        email = self.normalize_email(email)
        nickname = email.split('@')[0] if nickname == None else nickname
        user = self.model(
            email = email,
            password = password,
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname=None):
        email = self.normalize_email(email)
        nickname = email.split('@')[0] if nickname == None else nickname
        user = self.create_user(
            email = email,
            password = password,
            nickname = nickname,
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def follower_json():
    return {'follower_count':0}

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(validators = [RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')], max_length = 13, unique = True)
    image = models.URLField(max_length=250, null=True, blank=True)
    follower = models.JSONField(default=follower_json)
    created_at = models.DateTimeField(auto_now_add=True)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'nickname'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname
    
    @property
    def is_staff(self):
        return self.is_admin
