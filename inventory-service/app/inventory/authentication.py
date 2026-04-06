import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.extensions import OpenApiAuthenticationExtension



class InternalServiceUser:
    """
    Fake user object for internal service authentication.
    DRF requires request.user to exist and be authenticated.
    """

    is_authenticated = True

    def __str__(self):
        return "InternalServiceUser"


class InternalServiceAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationFailed("Missing Authorization header")

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid Authorization header")

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_aud": False},
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")

        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # ensure token is internal service token
        if payload.get("role") != "internal_service":
            raise AuthenticationFailed("Not an internal service token")

        # return authenticated service user
        return (InternalServiceUser(), payload)



class InternalAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'inventory.authentication.InternalServiceAuthentication'  # Use the full import path
    name = 'internalAuth'  # This MUST match the key in SPECTACULAR_SETTINGS

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Internal-Secret',
            'description': 'Shared secret for Service-to-Service communication',
        }