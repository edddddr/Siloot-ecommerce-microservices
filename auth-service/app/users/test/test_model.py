from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="StrongPass123"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("StrongPass123"))
        self.assertFalse(user.is_staff)