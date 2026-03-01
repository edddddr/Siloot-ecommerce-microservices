from django.urls import path
from .views import InternalTokenView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
     path("internal/token/", InternalTokenView.as_view()),
]