from django.urls import path, include

urlpatterns = [
    path("api/orders/", include("orders.urls")),
]