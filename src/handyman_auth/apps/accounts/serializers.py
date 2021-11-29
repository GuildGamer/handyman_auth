from rest_framework import serializers
from .models import HandyManBaseUser

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandyManBaseUser
        fields = [
            "email", "firstname", "lastname", "password", "phone"
        ]