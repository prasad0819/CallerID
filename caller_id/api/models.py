from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True, blank=True, null=True)
    phone_number = PhoneNumberField("phone number", unique=True, blank=False, null=False)
    full_name = models.CharField("full name", max_length=255, blank=False, null=False)

    # Adding the below to maintain parity with AbstractUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
    


