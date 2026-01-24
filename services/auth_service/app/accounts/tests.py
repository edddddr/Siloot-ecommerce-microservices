from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class AuthSmokeTest(APITestCase):
    def test_register_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {"email": "test@example.com", "password": "test12345"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)