from rest_framework import serializers


class ReserveStockSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class ReservationActionSerializer(serializers.Serializer):
    reservation_id = serializers.UUIDField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class ReservationNotFoundErrorSerializer(serializers.Serializer):
    error = serializers.CharField()