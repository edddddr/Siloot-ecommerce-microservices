from django.urls import path
from .views import CreateOrderView, OrderDetailView, UserOrdersView


urlpatterns = [

    path("orders/", CreateOrderView.as_view()),

    path("orders/<uuid:order_id>/", OrderDetailView.as_view()),

    path("orders/user/<uuid:user_id>/", UserOrdersView.as_view()),


]