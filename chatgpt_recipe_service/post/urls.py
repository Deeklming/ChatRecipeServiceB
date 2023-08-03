# blog/urls.py
from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('list/', views.PostsList.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('detail/<int:pk>/', views.PostDetailorUpdate.as_view()),
]
