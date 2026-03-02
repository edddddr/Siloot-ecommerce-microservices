from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User


class AuthAPITest(APITestCase):

    def setUp(self):
        self.register_url = "/api/v1/auth/register/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"

    def test_register_user(self):
        data = {
            "email": "test@example.com",
            "password": "StrongPass123",
            "first_name": "John",
            "last_name": "Doe"
        }

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_user(self):
        User.objects.create_user(
            email="test@example.com",
            password="StrongPass123"
        )

        data = {
            "email": "test@example.com",
            "password": "StrongPass123"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_logout_blacklist(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="StrongPass123"
        )

        login_response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "StrongPass123"
        })

        refresh_token = login_response.data["refresh"]

        response = self.client.post(self.logout_url, {
            "refresh": refresh_token
        })

        self.assertEqual(response.status_code, 205)