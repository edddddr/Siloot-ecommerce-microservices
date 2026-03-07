import uuid
from django.db import models


class InventoryItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product_id = models.UUIDField()

    total_stock = models.PositiveIntegerField()

    reserved_stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_items"
        indexes = [
            models.Index(fields=["product_id"]),
        ]

    def __str__(self):
        return f"InventoryItem {self.product_id}"


class StockReservation(models.Model):

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_RELEASED = "released"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_RELEASED, "Released"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order_id = models.UUIDField()

    product_id = models.UUIDField()

    quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stock_reservations"
        indexes = [
            models.Index(fields=["order_id"]),
            models.Index(fields=["product_id"]),
        ]

    def __str__(self):
        return f"Reservation {self.order_id}"