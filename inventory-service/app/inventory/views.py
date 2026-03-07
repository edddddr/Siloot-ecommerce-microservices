from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ReserveStockSerializer,
    ReservationActionSerializer
)

from .services import InventoryService


class ReserveStockView(APIView):

    def post(self, request):

        serializer = ReserveStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = InventoryService.reserve_stock(
            order_id=serializer.validated_data["order_id"],
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {
                "reservation_id": reservation.id,
                "status": reservation.status
            },
            status=status.HTTP_201_CREATED
        )


class ConfirmReservationView(APIView):

    def post(self, request):

        serializer = ReservationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = InventoryService.confirm_reservation(
            serializer.validated_data["reservation_id"]
        )

        return Response(
            {
                "reservation_id": reservation.id,
                "status": reservation.status
            }
        )

class ReleaseReservationView(APIView):

    def post(self, request):

        serializer = ReservationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = InventoryService.release_reservation(
            serializer.validated_data["reservation_id"]
        )

        return Response(
            {
                "reservation_id": reservation.id,
                "status": reservation.status
            }
        )
