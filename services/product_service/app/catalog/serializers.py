from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created_by_id"]


class ProductSerializer(serializers.ModelSerializer):
    # READ ONLY (output)
    category = CategorySerializer(read_only=True)

    # WRITE ONLY (input)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["created_by_id"]
