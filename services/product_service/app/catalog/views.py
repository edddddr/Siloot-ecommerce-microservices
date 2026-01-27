from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .authentication import AuthServiceAuthentication


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = [AuthServiceAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user.id)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [AuthServiceAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Category.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        print(f"DEBUG: Category fields are: {[f.name for f in Category._meta.get_fields()]}")
        serializer.save(created_by_id=self.request.user.id)
