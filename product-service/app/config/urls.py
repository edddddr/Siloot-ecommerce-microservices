from django.contrib import admin
from django.urls import path, include
from catalog.health import health_check
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("catalog.urls")),
    path("api/v1/health/", health_check),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path("api/docs/",
         SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger-ui"),

    path("api/redoc/",
         SpectacularRedocView.as_view(url_name="schema"),
         name="redoc")
]