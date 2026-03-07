import uuid
from django.db import transaction
from django.db.models import F

from .models import InventoryItem, StockReservation


class InventoryService:

    @staticmethod
    @transaction.atomic
    def reserve_stock(order_id, product_id, quantity):

        inventory = InventoryItem.objects.select_for_update().get(
            product_id=product_id
        )

        available_stock = inventory.total_stock - inventory.reserved_stock

        if available_stock < quantity:
            raise ValueError("Insufficient stock")

        inventory.reserved_stock = F("reserved_stock") + quantity
        inventory.save()

        reservation = StockReservation.objects.create(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
        )

        return reservation
    

    