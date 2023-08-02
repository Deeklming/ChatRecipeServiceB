# blog/urls.py
from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('list/', views.PostsList.as_view()),
    # path('like/<int:pk>/', views.like_post, name='like_post')
]
