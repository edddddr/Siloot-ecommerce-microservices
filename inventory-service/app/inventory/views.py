import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ReserveStockSerializer,
    ReservationActionSerializer
)

from .services.services import InventoryService
from rest_framework import status, serializers


from .authentication import InternalServiceAuthentication  
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from .services.cache import InventoryCache

from .exceptions import InsufficientStockError

from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)

class ReserveStockView(APIView):

    authentication_classes = [InternalServiceAuthentication]
    permission_classes = [IsAuthenticated]  

    @extend_schema(
        summary="Reserve stock for an order",
        description="Internal endpoint to temporarily reserve stock during the checkout process.",
        request=ReserveStockSerializer,
        responses={
            201: inline_serializer(
                name="ReservationSuccess",
                fields={
                    "reservation_id": serializers.UUIDField(),
                    "status": serializers.CharField()
                }
            ),
            400: inline_serializer(
                name="ReservationFailed",
                fields={"error": serializers.CharField(), "details": serializers.DictField()}
            ),
            409: inline_serializer(
                name="StockConflict",
                fields={"error": serializers.CharField()}
            ),
            500: inline_serializer(
                name="InternalError",
                fields={"error": serializers.CharField()}
            )
        }
    )
    
    def post(self, request):

        order_id = request.data.get("order_id")
        product_id = request.data.get("product_id")

        logger.info(
            "Stock reservation attempt received", 
            extra={"order_id": order_id, "product_id": product_id}
        )

        try:
            serializer = ReserveStockSerializer(data=request.data)
            if not serializer.is_valid():
                    logger.warning("Reservation validation failed", extra={"errors": serializer.errors})
                    return Response(
                        {"error": "Invalid request data", "details": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            reservation = InventoryService.reserve_stock(
                order_id=serializer.validated_data["order_id"],
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )

            logger.info(
                    "Stock reserved successfully", 
                    extra={"reservation_id": reservation.id, "order_id": order_id}
                )
            

            return Response(
                {
                    "reservation_id": reservation.id,
                    "status": reservation.status
                },
                status=status.HTTP_201_CREATED
            )

        except InsufficientStockError as e: 
            logger.warning(
                "Stock reservation rejected: Insufficient stock", 
                extra={"product_id": product_id, "order_id": order_id}
            )
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_409_CONFLICT
            )
        
        except Exception as e:
            # 4. Critical System Error
            logger.error(
                "Critical failure during stock reservation", 
                extra={"error": str(e), "order_id": order_id},
                exc_info=True
            )
            return Response(
                {"error": "Internal inventory service error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
@extend_schema(
    summary="Confirm stock reservation",
    description="Finalizes stock deduction after successful payment."
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


@extend_schema(
    summary="Release stock reservation",
    description="Releases reserved stock when payment fails or order is cancelled."
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


@extend_schema(
    summary="Get available stock",
    description="Returns available stock for a product (cached with Redis)."
)
@api_view(["GET"])
def get_stock(request, product_id):

    stock = InventoryCache.get_stock(product_id)

    return Response({
        "product_id": product_id,
        "available_stock": stock
    })