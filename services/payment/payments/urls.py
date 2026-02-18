from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import stripe_webhook
from .views import PaymentViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns = router.urls  + [
    path("payments/webhook/", stripe_webhook),
]