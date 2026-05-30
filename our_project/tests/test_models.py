import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile
from users.serializers import UserRegisterSerializer


@pytest.fixture
def category(db):
    return Category.objects.create(name="PinkStore", slug="pinkstore")


@pytest.fixture
def hoodie_product(db, category):
    return Product.objects.create(
        category=category,
        title="Розовое худи",
        description="Мягкое розовое худи в стиле PinkStore",
        price=Decimal("3500.00"),
        stock=10,
        is_available=True,
        image_path="img/products/hoodie_pink.jpg",
    )


@pytest.fixture
def earrings_product(db, category):
    return Product.objects.create(
        category=category,
        title="Серьги-бантики",
        description="Милые серьги-бантики",
        price=Decimal("1200.00"),
        stock=15,
        is_available=True,
        image_path="img/products/earrings_bows.jpg",
    )


@pytest.fixture
def mug_product(db, category):
    return Product.objects.create(
        category=category,
        title="Кружка с котиком",
        description="Розовая кружка с котиком",
        price=Decimal("400.00"),
        stock=20,
        is_available=True,
        image_path="img/products/cup_cat.jpg",
    )


@pytest.fixture
def tshirt_product(db, category):
    return Product.objects.create(
        category=category,
        title="Футболка Pink Love",
        description="Розовая футболка Pink Love",
        price=Decimal("1299.00"),
        stock=8,
        is_available=True,
        image_path="img/products/tshirt_pink.jpg",
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="pass12345"
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="bob",
        email="bob@example.com",
        password="pass12345"
    )


@pytest.fixture
def profile(db, user):
    return Profile.objects.create(
        user=user,
        phone="+79990000000",
        address="Казань"
    )


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)


@pytest.fixture
def review(db, user, hoodie_product):
    return Review.objects.create(
        product=hoodie_product,
        user=user,
        text="Очень красивое и удобное худи",
        rating=5,
    )


@pytest.mark.django_db
class TestCategoryModel:
    def test_str_returns_category_name(self, category):
        assert str(category) == "PinkStore"


@pytest.mark.django_db
class TestProductModel:
    def test_str_returns_title_and_price(self, hoodie_product):
        assert str(hoodie_product) == "Розовое худи (3500.00 руб.)"

    def test_default_stock_is_zero(self, category):
        product = Product.objects.create(
            category=category,
            title="Тестовый товар",
            description="Описание товара",
            price=Decimal("1000.00"),
        )
        assert product.stock == 0

    def test_default_is_available_is_true(self, category):
        product = Product.objects.create(
            category=category,
            title="Тестовый товар",
            description="Описание товара",
            price=Decimal("1000.00"),
        )
        assert product.is_available is True


@pytest.mark.django_db
class TestOrderModel:
    def test_default_status_is_pending(self, order):
        assert order.status == "pending"

    def test_default_is_paid_is_false(self, order):
        assert order.is_paid is False

    def test_str_returns_order_info(self, order, user):
        assert str(order) == f"Заказ #{order.id} от {user.username}"

    def test_calculate_total_sums_all_items(self, order, hoodie_product, mug_product):
        OrderItem.objects.create(
            order=order,
            product=hoodie_product,
            price=Decimal("3500.00"),
            quantity=2
        )
        OrderItem.objects.create(
            order=order,
            product=mug_product,
            price=Decimal("400.00"),
            quantity=1
        )

        total = order.calculate_total()

        assert total == Decimal("7400.00")
        order.refresh_from_db()
        assert order.total_price == Decimal("7400.00")


@pytest.mark.django_db
class TestOrderItemModel:
    def test_get_cost_returns_price_multiplied_by_quantity(self, order, earrings_product):
        item = OrderItem.objects.create(
            order=order,
            product=earrings_product,
            price=Decimal("1200.00"),
            quantity=3
        )
        assert item.get_cost() == Decimal("3600.00")

    def test_price_is_taken_from_product_if_not_set(self, order, tshirt_product):
        item = OrderItem.objects.create(
            order=order,
            product=tshirt_product,
            quantity=2
        )
        assert item.price == Decimal("1299.00")

    def test_order_total_is_updated_after_item_save(self, order, mug_product):
        OrderItem.objects.create(
            order=order,
            product=mug_product,
            price=Decimal("400.00"),
            quantity=2
        )
        order.refresh_from_db()
        assert order.total_price == Decimal("800.00")

    def test_price_snapshot_does_not_change_if_product_price_changes(self, order, hoodie_product):
        item = OrderItem.objects.create(
            order=order,
            product=hoodie_product,
            quantity=1
        )

        assert item.price == Decimal("3500.00")

        hoodie_product.price = Decimal("3900.00")
        hoodie_product.save()

        item.refresh_from_db()
        assert item.price == Decimal("3500.00")


@pytest.mark.django_db
class TestReviewModel:
    def test_str_returns_expected_text(self, review):
        assert str(review) == f"Отзыва от {review.user.username} на {review.product.title}"

    def test_review_is_linked_to_correct_user_and_product(self, review, user, hoodie_product):
        assert review.user == user
        assert review.product == hoodie_product
        assert review.rating == 5

    def test_review_has_created_at(self, review):
        assert review.created_at is not None


@pytest.mark.django_db
class TestProfileModel:
    def test_str_returns_username(self, profile, user):
        assert str(profile) == f"Профиль {user.username}"


@pytest.mark.django_db
class TestUserRegisterSerializer:
    def test_validate_fails_if_passwords_do_not_match(self):
        serializer = UserRegisterSerializer(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "password_confirm": "different123",
            "first_name": "Test",
            "last_name": "User",
        })

        assert serializer.is_valid() is False
        assert "non_field_errors" in serializer.errors

    def test_create_user_and_profile_when_data_is_valid(self):
        serializer = UserRegisterSerializer(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "password_confirm": "password123",
            "first_name": "Test",
            "last_name": "User",
        })

        assert serializer.is_valid(), serializer.errors
        user = serializer.save()

        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert Profile.objects.filter(user=user).exists() is True