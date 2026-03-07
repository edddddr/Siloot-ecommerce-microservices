from django.urls import path

from .views import (
    ReserveStockView,
    ConfirmReservationView,
    ReleaseReservationView,
)

urlpatterns = [
    path("reserve/", ReserveStockView.as_view()),
    path("confirm/", ConfirmReservationView.as_view()),
    path("release/", ReleaseReservationView.as_view()),
]