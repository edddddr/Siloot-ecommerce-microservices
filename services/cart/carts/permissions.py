import requests
from django.conf import settings
from rest_framework.permissions import BasePermission

class IsAuthenticatedViaAuthService(BasePermission):

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return False

        response = requests.get(
            f"{settings.AUTH_SERVICE_URL}/profile/me",
            headers={"Authorization": auth_header}
        )

        if response.status_code != 200:
            return False

        request.user_data = response.json()
        return True