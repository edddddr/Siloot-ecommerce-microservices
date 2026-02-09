from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, RegisterView, MeView

urlpatterns = [
    # auth
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # users
    path("users/", RegisterView.as_view(), name="register"),
    path("users/me/", MeView.as_view(), name="me"),
]
