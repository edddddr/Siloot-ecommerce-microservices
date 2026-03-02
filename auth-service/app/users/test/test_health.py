from rest_framework.test import APITestCase


class HealthCheckTest(APITestCase):

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/auth/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")