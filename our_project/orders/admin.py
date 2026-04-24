from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline для позиций заказа"""
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'get_cost']
    fields = ['product', 'quantity', 'price', 'get_cost']

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Стоимость'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin для заказов"""
    list_display = ('id', 'user', 'status', 'is_paid', 'total_price', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status', 'is_paid')
        }),
        ('Финансы', {
            'fields': ('total_price',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin для позиций заказа"""
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'get_cost')
    list_filter = ('order__status',)
    search_fields = ('product__title', 'order__id')

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Стоимость'