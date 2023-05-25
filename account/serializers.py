from django.contrib.auth import get_user_model
from .models import User

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class CreateUserSerializer(ModelSerializer):
    phone = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'phone', 'email')

    def create(self, validated_data):
        return User.objects._create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)