from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Category, Product
from reviews.models import Review
from orders.models import Order, OrderItem
from users.models import Profile
from faker import Faker
import random

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Начинаем заполнение базы данных...'))

        # 1. Создание администратора
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pinkstore.ru',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('✅ Создан администратор: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Администратор уже существует'))

        # 2. Создание обычных пользователей
        users_data = [
            ('user1', 'user1@mail.ru'),
            ('user2', 'user2@mail.ru'),
            ('user3', 'user3@mail.ru'),
            ('zarinagimazova', 'zarinagimazova@mail.ru'),
        ]

        users = []
        for username, email in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Создан пользователь: {username}'))
            users.append(user)

        # 3. Создание профилей для пользователей
        for user in users:
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f'+7{random.randint(9000000000, 9999999999)}',
                    'address': fake.address(),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создан профиль для: {user.username}'))

        # 4. Создание категорий товаров
        categories_data = [
            ('Кружки', 'cups'),
            ('Футболки', 'tshirts'),
            ('Сумки', 'bags'),
            ('Аксессуары', 'accessories'),
            ('Плакаты', 'posters'),
        ]

        categories = []
        for name, slug in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создана категория: {name}'))
            categories.append(category)

        # 5. Создание товаров
        products_data = [
            ('Кружка с котиком', 'img/products/cup_cat.jpg', categories[0], 599.00,
             'Милая керамическая кружка с рисунком котика'),
            (
            'Кружка с сердечками', 'img/products/cup_hearts.jpg', categories[0], 499.00, 'Кружка с узором из сердечек'),
            ('Футболка Pink Love', 'img/products/tshirt_pink.jpg', categories[1], 1299.00,
             'Розовая футболка с надписью Love'),
            (
            'Футболка с котом', 'img/products/tshirt_cat.jpg', categories[1], 1199.00, 'Белая футболка с принтом кота'),
            ('Сумка розовая', 'img/products/bag_pink.jpg', categories[2], 899.00, 'Модная розовая сумка'),
            ('Сумка с принтом', 'img/products/bag_print.jpg', categories[2], 999.00, 'Сумка с милым принтом'),
            ('Брелок сердечко', 'img/products/keychain.jpg', categories[3], 199.00, 'Брелок в форме сердечка'),
            ('Плакат с котиками', 'img/products/poster_cat.jpg', categories[4], 399.00,
             'Плакат с котиками для интерьера'),
            ('Кружка с зайкой', 'img/products/cup_bunny.jpg', categories[0], 649.00, 'Кружка с милым зайкой'),
            ('Футболка с зайкой', 'img/products/tshirt_bunny.jpg', categories[1], 1399.00, 'Футболка с принтом зайки'),
        ]

        products = []
        for title, image_path, category, price, description in products_data:
            product, created = Product.objects.get_or_create(
                title=title,
                defaults={
                    'category': category,
                    'description': description,
                    'price': price,
                    'stock': random.randint(5, 50),
                    'is_available': True,
                    'image_path': image_path,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создан товар: {title}'))
            products.append(product)

        # 6. Создание отзывов
        for product in products:
            for user in random.sample(users, min(2, len(users))):
                review, created = Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'text': fake.text(max_nb_chars=200),
                        'rating': random.randint(3, 5),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✅ Создан отзыв от {user.username} на {product.title}'))

        # 7. Создание заказов с позициями
        for user in users:
            for _ in range(random.randint(1, 3)):
                # Создаём заказ
                order = Order.objects.create(
                    user=user,
                    status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                    is_paid=random.choice([True, False])
                )

                # Добавляем 1-3 товара в заказ
                selected_products = random.sample(products, random.randint(1, 3))
                for product in selected_products:
                    quantity = random.randint(1, 2)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity
                    )

                # Пересчитываем сумму
                order.calculate_total()

                self.stdout.write(self.style.SUCCESS(f'✅ Создан заказ #{order.id} для {user.username}'))

        self.stdout.write(self.style.SUCCESS('🎉 База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Итого:'))
        self.stdout.write(self.style.SUCCESS(f'   - Пользователей: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Категорий: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Товаров: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Отзывов: {Review.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Заказов: {Order.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Позиций заказов: {OrderItem.objects.count()}'))