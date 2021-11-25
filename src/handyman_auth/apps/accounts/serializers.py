from rest_framework import serializers
from .models import HandyManUser

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandyManUser
        fields = [

        ]