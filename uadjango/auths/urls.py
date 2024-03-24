from django.urls import path
from . import views

app_name = 'auths'

urlpatterns = [
    path("users/all/", views.GetAllUsers.as_view(), name='get_all_users'),
    path("users/create/", views.CreateUser.as_view(), name='create_user'),
]