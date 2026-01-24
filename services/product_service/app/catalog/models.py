from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = TreeForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )
    tags = TaggableManager(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name