from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    is_paid = models.BooleanField('Оплачен', default=False)
    total_price = models.DecimalField(
        'Общая сумма',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    def calculate_total(self):
        """Пересчитать общую сумму заказа"""
        total = sum(item.get_cost() for item in self.items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])
        return total


class OrderItem(models.Model):
    """Позиция в заказе"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    price = models.DecimalField(
        'Цена за единицу',
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def get_cost(self):
        """Стоимость позиции"""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Если цена не указана, берём текущую цену товара
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        # Пересчитываем общую сумму заказа
        self.order.calculate_total()