from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta


class InternalServiceToken(AccessToken):
    lifetime = timedelta(minutes=5)

    @classmethod
    def for_service(cls, service_name: str):
        token = cls()
        token["service"] = service_name
        token["role"] = "internal_service"
        token["iss"] = "auth-service"
        return token