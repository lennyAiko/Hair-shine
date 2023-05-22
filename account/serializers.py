from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Profile

User = get_user_model()

def creator(data, model):
    user = model.objects.create_user(
        username = data['username'],
        first_name = data['first_name'],
        last_name = data['last_name'],
        password = data['password'],
        email = data['email']
    )
    Profile.objects.create(
        user = user,
        phone = data['phone'],
    )
    return True

class CreateUserSerializer(ModelSerializer):
    phone = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'phone', 'email')

    def create(self, validated_data):
        return creator(validated_data, User)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('user', 'phone', 'location')  

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)