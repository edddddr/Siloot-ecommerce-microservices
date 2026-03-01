from django.urls import path
from .views import InternalTokenView, RegisterView, LoginView, LogoutView
from .health import HealthCheckView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]

urlpatterns += [
    path("internal/token/", InternalTokenView.as_view()),
    path("health/", HealthCheckView.as_view()),
]