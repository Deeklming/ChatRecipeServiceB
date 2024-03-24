from rest_framework import serializers
from .models import Hashtags

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtags
        fields = '__all__'
