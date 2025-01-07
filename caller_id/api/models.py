from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, blank=False, null=False)
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
    
    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['full_name']),
        ]
    
class Contact(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    owner = models.ForeignKey(CustomUser, blank=False, null=True, on_delete=models.SET_NULL, related_name='contacts')
    
    def __str__(self):
        return self.full_name + ", " + str(self.phone_number)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number', 'owner'], name='unique_owner_contact')
        ]

        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['full_name']),
        ]
    
class SpamReport(models.Model):
    phone_number = PhoneNumberField(blank=False, null=False)
    reported_by = models.ForeignKey(CustomUser, blank=False, null=True, on_delete=models.SET_NULL, related_name='spam_reports')
    
    def __str__(self):
        return str(self.phone_number)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number', 'reported_by'], name='unique_spam_report')
        ]

        indexes = [
            models.Index(fields=['phone_number']),

        ]
    

    


