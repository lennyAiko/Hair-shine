from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    """
    User Profile Model
    Defines the attributes of a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
    
    def __repr__(self) -> str:
        return f'{self.user.username} is added'