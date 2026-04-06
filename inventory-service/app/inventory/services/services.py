import uuid
from django.db import transaction
from django.db.models import F

from inventory.models import InventoryItem, StockReservation

from .cache import InventoryCache

from inventory.exceptions import InsufficientStockError, ReservationIsProcessed


class InventoryService:

    @staticmethod
    @transaction.atomic
    def reserve_stock(order_id, product_id, quantity):

        inventory = InventoryItem.objects.select_for_update().get(
            product_id=product_id
        )

        available_stock = inventory.total_stock - inventory.reserved_stock

        if available_stock < quantity:
            raise InsufficientStockError()

        inventory.reserved_stock = F("reserved_stock") + quantity
        inventory.save()

        reservation = StockReservation.objects.create(

            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
        )

        InventoryCache.invalidate_stock(product_id)

        return reservation
    

    @staticmethod
    @transaction.atomic
    def confirm_reservation(reservation_id):

        reservation = StockReservation.objects.select_for_update().get(
            id=reservation_id
        )

        if reservation.status != StockReservation.STATUS_PENDING:
            raise ReservationIsProcessed

        inventory = InventoryItem.objects.select_for_update().get(
            product_id=reservation.product_id
        )

        inventory.total_stock = F("total_stock") - reservation.quantity
        inventory.reserved_stock = F("reserved_stock") - reservation.quantity
        inventory.save()

        reservation.status = StockReservation.STATUS_CONFIRMED
        reservation.save()

        InventoryCache.invalidate_stock(reservation.product_id)

        return reservation


    @staticmethod
    @transaction.atomic
    def release_reservation(reservation_id):

        reservation = StockReservation.objects.select_for_update().get(
            id=reservation_id
        )

        if reservation.status != StockReservation.STATUS_PENDING:
            raise ValueError("Reservation already processed")

        inventory = InventoryItem.objects.select_for_update().get(
            product_id=reservation.product_id
        )

        inventory.reserved_stock = F("reserved_stock") - reservation.quantity
        inventory.save()

        reservation.status = StockReservation.STATUS_RELEASED
        reservation.save()

        InventoryCache.invalidate_stock(reservation.product_id)

        return reservation
        