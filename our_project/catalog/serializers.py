from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'stock',
            'is_available', 'image_path', 'image_url',
            'category', 'category_name'
        ]
        read_only_fields = ['id']

    def get_image_url(self, obj):
        if obj.image_path:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(f'/static/{obj.image_path}')
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category_name', 'is_available', 'image_path']