from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart),
    path("items/", views.add_to_cart),
    path("items/<int:product_id>/", views.remove_from_cart),
    path("clear/", views.clear),
]