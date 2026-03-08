from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product_id", "quantity")