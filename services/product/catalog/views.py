from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache


from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOrSeller

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSeller]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSeller]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        query_params = request.query_params.urlencode()
        cache_key = f"product_list_{query_params}" if query_params else "product_list_all"

        print(f"DEBUG: Looking for Key: {cache_key}")
        data = cache.get(cache_key)

        if not data:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)
        

        return Response(data)

    def clear_product_cache(self):
        cache.delete_pattern("product_list_*")

    def perform_create(self, serializer):
        serializer.save()
        self.clear_product_cache()

    def perform_update(self, serializer):
        serializer.save()
        self.clear_product_cache()

    def perform_destroy(self, instance):
        instance.delete()
        self.clear_product_cache()
