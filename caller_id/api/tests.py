from django.test import TestCase
from .models import CustomUser

class CustomUserManagerTests(TestCase):
    def test_password_is_hashed(self):
        user = CustomUser.objects.create_user(phone_number="+12345678904", password="testpassword")
        self.assertNotEqual(user.password, "testpassword")
        self.assertTrue(user.check_password("testpassword"))
