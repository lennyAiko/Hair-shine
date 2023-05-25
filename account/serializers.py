from .models import User

from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'password', 'phone')

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
        fields = ('email', 'last_name', 'first_name', 'phone', )

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)