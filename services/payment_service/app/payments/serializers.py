from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order_id",
            "amount",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]