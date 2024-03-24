from django.db import models
from datetime import datetime, timezone
from email_validator import validate_email, EmailNotValidError, caching_resolver
from django.contrib.postgres.fields import ArrayField
import uuid
import hashlib
import re

# Create your models here.
class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=True, db_index=True)
    email = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    password_last = models.JSONField(default=dict)
    business = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=datetime.now(timezone.utc))
    created_at = models.DateTimeField(default=datetime.now(timezone.utc))
    deleted_at = models.DateTimeField(null=True, default=None)
    status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name
    
    def digest_password(self, pw: str):
        return hashlib.sha3_512(pw.encode()).hexdigest()
    
    def check_password(self, pw: str):
        return self.password == self.digest_password(pw)
    
    def validate_id(n: str, e: str):
        # 유저 이름 검증
        if not re.compile('^(?=.*[\\w])[\\w]{2,20}$').search(n):
            return (False, 'name validate failed')
        # 이메일 검증
        try:
            emailinfo = validate_email(e, check_deliverability=True, dns_resolver=caching_resolver(timeout=5))
            email = emailinfo.normalized
            return (True, 'id success')
        except EmailNotValidError as err:
            print(err)
            return (False, 'email validate failed')
    
    def validate_password(self, pw: str):
        # 현재 및 과거 중복된 PW
        hash_pw = self.digest_password(pw)
        if self.password_last:
            for x in self.password_last.values():
                if self.password == hash_pw:
                    return (False, 'overlapping password')
        # 영문자, 숫자, 특수문자 최소 하나씩 8~32자 검증
        r = re.compile('^(?=.*[\\d])(?=.*[a-zA-Z])(?=.*[\\W])[\\S]{8,32}$').fullmatch(pw)
        if not r:
            return (False, 'password condition check failed')
        # 특정 패턴 검증
        ptrn = [
            re.compile('(\\w)\\1\\1').findall(pw), #3자 이상 연속된 동일 문자
            re.compile(f'(?i){self.name}|{self.email.split("@")[0]}').search(pw) #유저 이름, 이메일 아이디 포함
        ]
        for x in ptrn:
            if x:
                return (False, 'password easy pattern')
        return (True, 'password success')


class Profiles(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    image = models.URLField(max_length=150, null=True, default=None)
    nationality = models.CharField(max_length=2)
    like = models.JSONField(default=dict)
    accommodation = ArrayField(models.CharField(max_length=30, blank=True), default=list)
    clip = ArrayField(models.IntegerField(), default=list)
    follow = ArrayField(models.UUIDField(), default=list)
    comment = ArrayField(models.IntegerField(), default=list)

    def __str__(self) -> str:
        return self.user_id
