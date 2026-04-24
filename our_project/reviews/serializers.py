from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    stars_display = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'user_username',
            'product_title', 'text', 'rating',
            'stars_display', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def get_stars_display(self, obj):
        return '⭐' * obj.rating


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов"""

    class Meta:
        model = Review
        fields = ['product', 'text', 'rating']