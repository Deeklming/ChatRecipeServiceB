from django.contrib import admin
from .models import Users, Profiles

# Register your models here.
admin.site.register(Users) # admin 페이지에 등록
admin.site.register(Profiles)
