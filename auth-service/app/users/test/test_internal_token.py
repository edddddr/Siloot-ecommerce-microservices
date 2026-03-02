from rest_framework.test import APITestCase
import os


class InternalTokenTest(APITestCase):

    def setUp(self):
        self.url = "/api/v1/auth/internal/token/"

    def test_internal_token_success(self):
        response = self.client.post(
            self.url,
            {"service_name": "order-service"},
            HTTP_X_INTERNAL_SECRET=os.getenv("INTERNAL_SERVICE_SECRET")
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_internal_token_fail(self):
        response = self.client.post(
            self.url,
            {"service_name": "order-service"},
            HTTP_X_INTERNAL_SECRET="wrong-secret"
        )

        self.assertEqual(response.status_code, 403)