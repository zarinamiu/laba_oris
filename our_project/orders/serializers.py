from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции заказа"""
    product_title = serializers.CharField(source='product.title', read_only=True)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'price', 'quantity', 'cost']
        read_only_fields = ['id', 'price', 'cost']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания позиции заказа"""

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_username', 'status', 'status_display',
            'is_paid', 'total_price', 'items', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.items.count()


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказов"""
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Заказ должен содержать хотя бы одну позицию")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Недостаточно товара '{product.title}' на складе. Доступно: {product.stock}"
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity
            )

            product.stock -= quantity
            product.save()

        order.calculate_total()

        return order