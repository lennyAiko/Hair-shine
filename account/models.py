from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, role: str, phone: str, first_name: str, last_name: str, email: str, password: str = None, is_staff=True, is_superuser=False, is_verified=False) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have an first name")
        if not last_name:
            raise ValueError("User must have an last name")
        if not phone:
            raise ValueError("User must have a phone number")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_verified = is_verified
        user.role = role
        user.save()

        return user

    def create_user(self, phone: str, first_name: str, last_name: str, email: str, password: str = None, is_staff=True, is_superuser=False, is_verified=False, role="client") -> "User":
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            role=role
        )
        user.save()

        return user

    def create_superuser(self, phone: str, first_name: str, last_name: str, email: str, password: str = None, is_staff=True, is_superuser=True, is_verified=True, role="admin") -> "User":
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            is_staff=True,
            is_superuser=True,
            is_verified=True,
            role=role
        )
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    role = models.CharField(max_length=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, null=True, blank=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "role"]

    def __str__(self):
        return self.email

    # def get_full_details(self):
    #     return {
    #         self.email, self.first_name, self.last_name, self.phone, self.role
    #     }

    def find_by_email(self, email):
        return self.objects.filter(email=email)

    def get_details(self, email):
        user = self.objects.get(email=email)
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        }
        return data

    @property
    def isSuperuser(self):
        return self.is_superuser

    @property
    def isVerified(self):
        return self.is_verified
