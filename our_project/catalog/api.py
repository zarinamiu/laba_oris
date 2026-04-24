from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer


class CategoryListView(generics.ListAPIView):
    """API: Список всех категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список всех категорий товаров",
        responses={200: CategorySerializer(many=True)},
        tags=['Категории']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveAPIView):
    """API: Детальная информация о категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Получить информацию о категории по ID",
        responses={200: CategorySerializer()},
        tags=['Категории']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductListView(generics.ListAPIView):
    """API: Список всех товаров"""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список всех товаров",
        responses={200: ProductListSerializer(many=True)},
        tags=['Товары']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    """API: Детальная информация о товаре"""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о товаре по ID",
        responses={200: ProductSerializer()},
        tags=['Товары']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)