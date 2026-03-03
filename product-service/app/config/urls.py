from django.urls import path, include
from catalog.health import health_check


urlpatterns = [
    path("api/v1/", include("catalog.urls")),
    path("api/v1/health/", health_check),
]