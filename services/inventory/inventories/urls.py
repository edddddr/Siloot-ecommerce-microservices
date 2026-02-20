from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_inventory),
    path("<int:product_id>/", views.get_inventory),
    path("reserve/", views.reserve),
    path("release/", views.release),
    path("deduct/", views.deduct),
]