from django.contrib import admin
from .models import InventoryItem, StockReservation


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("product_id", "total_stock", "reserved_stock")


@admin.register(StockReservation)
class StockReservationAdmin(admin.ModelAdmin):
    list_display = ("order_id", "product_id", "quantity", "status")