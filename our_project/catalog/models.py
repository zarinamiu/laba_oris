from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Остаток на складе', default=0)
    is_available = models.BooleanField('В продаже', default=True)
    image_path = models.CharField(
        'Путь к картинке',
        max_length=255,
        blank=True,
        help_text='img/products/cup_cat.jpg'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.title} ({self.price} руб.)"