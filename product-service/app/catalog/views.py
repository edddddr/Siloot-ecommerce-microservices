from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .pagination import ProductCursorPagination

# Permission and Authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUserRole

# For cutsome Look up
import uuid
from django.shortcuts import get_object_or_404

# caching
from django.core.cache import cache
from rest_framework.response import Response
from .services.cache import (
    get_product_list_cache_key,
    cache_product_list,
    get_product_detail_cache_key,
    cache_product_detail,
)
from .services.cache import invalidate_product_cache


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ProductCursorPagination

    def get_object(self):
        """
        Custom lookup to support both UUID (pk) and Slug
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # 'pk' is the default name for the variable in the URL
        lookup_value = self.kwargs.get('pk')

        # 1. Check if the value is a valid UUID
        try:
            uuid_obj = uuid.UUID(str(lookup_value))
            # If valid UUID, look up by ID
            obj = get_object_or_404(queryset, id=uuid_obj)
        except (ValueError, AttributeError):
            # 2. If not a UUID, treat it as a slug
            obj = get_object_or_404(queryset, slug=lookup_value)

        self.check_object_permissions(self.request, obj)
        return obj

    

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]        
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUserRole()]

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    pagination_class = ProductCursorPagination

    # def get_object(self):
    #     return Product.objects.first()

    def get_object(self):
        """
        Custom lookup to support both UUID (pk) and Slug
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # 'pk' is the default name for the variable in the URL
        lookup_value = self.kwargs.get('pk')

        # Debugging: See what value is coming from the URL
        
        try:
            uuid_obj = uuid.UUID(str(lookup_value))
            
            # If valid UUID, look up by ID
            obj = get_object_or_404(queryset, id=uuid_obj)
        except (ValueError, AttributeError):
            # 2. If not a UUID, treat it as a slug
            
            obj = get_object_or_404(queryset, slug=lookup_value)

        self.check_object_permissions(self.request, obj)
        return obj
      

    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]        
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUserRole()]
    
    


    # Caching | redis 
    def list(self, request, *args, **kwargs):
        cache_key = get_product_list_cache_key(request.query_params)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        cache_product_list(cache_key, response.data)
    
        return response
    

    def retrieve(self, request, *args, **kwargs):
    # Use 'pk' because that is what the router sends, 
    # even if the value inside is actually a slug string.
        lookup_value = kwargs.get("pk") 
        cache_key = get_product_detail_cache_key(lookup_value)
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        
        # Only cache if the request was successful (200 OK)
        if response.status_code == 200:
            cache_product_detail(cache_key, response.data)

        return response
    
    def perform_create(self, serializer):
        instance = serializer.save()
        invalidate_product_cache()
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        invalidate_product_cache()
        return instance

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_product_cache()



