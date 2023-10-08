from django.urls import path
from . import views

urlpatterns =[
    path('userall/', views.UserAll.as_view()),
]
