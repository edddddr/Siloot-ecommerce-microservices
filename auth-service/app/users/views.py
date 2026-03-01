from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .tokens import InternalServiceToken
from rest_framework.throttling import ScopedRateThrottle


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class InternalTokenView(APIView):
    permission_classes = [AllowAny]  # we secure it differently

    def post(self, request):
        shared_secret = request.headers.get("X-Internal-Secret")

        if shared_secret != "internal-secret-key":
            return Response({"error": "Unauthorized"}, status=403)

        service_name = request.data.get("service_name")

        if not service_name:
            return Response({"error": "service_name required"}, status=400)

        token = InternalServiceToken.for_service(service_name)

        return Response({"access": str(token)})