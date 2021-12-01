from rest_framework import serializers
from .models import HandyManBaseUser


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandyManBaseUser
        fields = ["id", "email", "firstname", "lastname", "password", "phone"]

    extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
