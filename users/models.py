from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class MyModel(models.Model):
    class ProfileGender(models.TextChoices):
        MAL = 'Male', "Mężczyzna"
        FEM = 'Female', "Kobieta"
        UNN = 'Unknown', "Nie Wybrano"

    class BabyGender(models.TextChoices):
        BOY = 'Man', "Mężczyzna"
        GRL = "Woman", "Kobieta"
        UNN = 'Unknown', "Nie Wybrano"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    profile_birth = models.DateField()
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=11, choices=MyModel.ProfileGender.choices, default=MyModel.ProfileGender.UNN)

