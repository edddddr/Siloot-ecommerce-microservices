import requests
from django.conf import settings
from rest_framework.permissions import BasePermission

class IsAuthenticatedViaAuthService(BasePermission):

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        print(auth_header, '\n', settings.AUTH_SERVICE_URL)

        if not auth_header:
            return False

        # response = requests.get("http://127.0.0.1:8000/api/v1/auth/me/",
        #     headers={"Authorization": auth_header}

        # )

        response = requests.get(
            f"{settings.AUTH_SERVICE_URL}/auth/me/",
            headers={"Authorization": auth_header},
            timeout=2
        )

        if response.status_code != 200:
            print("Auth service response: ", response.text)
            return False

        request.user_data = response.json()
        return True