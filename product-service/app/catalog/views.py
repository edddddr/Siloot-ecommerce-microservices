from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .pagination import ProductCursorPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    pagination_class = None
    lookup_value_regex = "[0-9a-f-]{36}|[-\w]+"

    filterset_fields = ["parent"]  # Explicit only
    search_fields = ["name"]
    ordering_fields = ["created_at", "name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUserRole()]
        return [IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    pagination_class = ProductCursorPagination

    


    filterset_fields = {
        "category": ["exact"], 
        "is_active": ["exact"],
    }
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUserRole()]
        return [IsAuthenticated()]


