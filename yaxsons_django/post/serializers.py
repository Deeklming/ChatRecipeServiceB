from rest_framework import serializers
from .models import Post, Comment

class PostAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

