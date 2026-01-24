from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({"get": "list"})
add_item = CartViewSet.as_view({"post": "add_item"})
remove_item = CartViewSet.as_view({"delete": "remove_item"})

urlpatterns = [
    path("", cart_list),
    path("add-item/", add_item),
    path("remove-item/<int:pk>/", remove_item),
]