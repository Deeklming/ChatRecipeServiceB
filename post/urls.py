from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from django.conf.urls.static import static
# from django.conf import settings
from . import views

urlpatterns =[
    path('postall/', views.PostAll.as_view()),
    path('commentall/', views.CommentAll.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)