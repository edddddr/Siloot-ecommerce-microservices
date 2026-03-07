from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ReserveStockSerializer,
    ReservationActionSerializer
)

from .services import InventoryService


from .authentication import InternalServiceAuthentication  
from rest_framework.permissions import IsAuthenticated

class ReserveStockView(APIView):

    authentication_classes = [InternalServiceAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [InternalServiceAuthentication]
    permission_classes = [IsAuthenticated]    

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
    authentication_classes = [InternalServiceAuthentication]
    permission_classes = [IsAuthenticated]    

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
