from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.phonenumber import PhoneNumber


# CustomUserManager to use phone number instead of username for User
class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        
        phone_number = PhoneNumber.from_string(phone_number)

        if not phone_number.is_valid():
            raise ValueError("The Phone Number is not valid")
        
        user = self.model(phone_number=phone_number.as_e164, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number, password, **extra_fields)