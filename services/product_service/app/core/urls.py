from django.urls import path, include

urlpatterns = [
    path("api/catalog/", include("catalog.urls")),  
]