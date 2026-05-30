import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile


@pytest.fixture
def api_client():
    return APIClient()


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
def empty_image_product(db, category):
    return Product.objects.create(
        category=category,
        title="Розовая заколка",
        description="Заколка без картинки",
        price=Decimal("250.00"),
        stock=5,
        is_available=True,
        image_path="",
    )


@pytest.fixture
def review(db, user, hoodie_product):
    return Review.objects.create(
        product=hoodie_product,
        user=user,
        text="Очень красивое и удобное худи",
        rating=5,
    )


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)


@pytest.fixture
def another_user_order(db, another_user):
    return Order.objects.create(user=another_user)


@pytest.fixture
def order_item(db, order, hoodie_product):
    return OrderItem.objects.create(
        order=order,
        product=hoodie_product,
        price=Decimal("3500.00"),
        quantity=2
    )


@pytest.mark.django_db
class TestCatalogAPI:
    def test_category_list_returns_200_and_data(self, api_client, category, hoodie_product):
        url = reverse("catalog:api_category_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 1

        category_data = response.data["results"][0]
        assert category_data["name"] == "PinkStore"
        assert category_data["slug"] == "pinkstore"
        assert category_data["products_count"] == 1

    def test_category_detail_returns_correct_category(self, api_client, category):
        url = reverse("catalog:api_category_detail", kwargs={"id": category.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == category.id
        assert response.data["name"] == "PinkStore"
        assert response.data["slug"] == "pinkstore"

    def test_product_list_returns_200_and_data(self, api_client, hoodie_product):
        url = reverse("catalog:api_product_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 1

        product_data = response.data["results"][0]
        assert product_data["title"] == "Розовое худи"
        assert product_data["price"] == "3500.00"
        assert product_data["category_name"] == "PinkStore"
        assert product_data["is_available"] is True

    def test_product_detail_returns_image_url(self, api_client, tshirt_product):
        url = reverse("catalog:api_product_detail", kwargs={"id": tshirt_product.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["title"] == "Футболка Pink Love"
        assert response.data["category_name"] == "PinkStore"
        assert response.data["image_path"] == "img/products/tshirt_pink.jpg"
        assert response.data["image_url"] is not None
        assert "/static/img/products/tshirt_pink.jpg" in response.data["image_url"]

    def test_product_detail_returns_null_image_url_if_image_path_empty(self, api_client, empty_image_product):
        url = reverse("catalog:api_product_detail", kwargs={"id": empty_image_product.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["image_url"] is None


@pytest.mark.django_db
class TestUsersAPI:
    def test_user_list_returns_200(self, api_client, user, profile):
        url = reverse("users:api_user_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 1

        user_data = response.data["results"][0]
        assert user_data["username"] == "alice"
        assert user_data["email"] == "alice@example.com"
        assert "profile" in user_data

    def test_user_detail_returns_200_and_correct_user(self, api_client, user, profile):
        url = reverse("users:api_user_detail", kwargs={"id": user.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["username"] == "alice"
        assert response.data["email"] == "alice@example.com"
        assert response.data["profile"]["phone"] == "+79990000000"

    def test_profile_endpoint_requires_auth(self, api_client):
        url = reverse("users:api_profile")
        response = api_client.get(url)

        assert response.status_code in (401, 403)

    def test_profile_endpoint_returns_current_user_profile_for_authenticated_user(self, api_client, user, profile):
        api_client.force_authenticate(user=user)
        url = reverse("users:api_profile")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["username"] == "alice"
        assert response.data["email"] == "alice@example.com"
        assert response.data["phone"] == "+79990000000"
        assert response.data["address"] == "Казань"

    def test_register_endpoint_creates_user_and_profile(self, api_client):
        url = reverse("users:api_register")
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "password_confirm": "password123",
            "first_name": "New",
            "last_name": "User",
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 201
        assert User.objects.filter(username="newuser").exists() is True

        created_user = User.objects.get(username="newuser")
        assert Profile.objects.filter(user=created_user).exists() is True

    def test_register_endpoint_returns_400_if_passwords_do_not_match(self, api_client):
        url = reverse("users:api_register")
        payload = {
            "username": "baduser",
            "email": "baduser@example.com",
            "password": "password123",
            "password_confirm": "otherpassword",
            "first_name": "Bad",
            "last_name": "User",
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 400
        assert User.objects.filter(username="baduser").exists() is False


@pytest.mark.django_db
class TestReviewsAPI:
    def test_review_list_returns_200(self, api_client, review):
        url = reverse("reviews:api_review_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 1

        review_data = response.data["results"][0]
        assert review_data["text"] == "Очень красивое и удобное худи"
        assert review_data["rating"] == 5
        assert review_data["user_username"] == "alice"
        assert review_data["product_title"] == "Розовое худи"
        assert review_data["stars_display"] == "⭐⭐⭐⭐⭐"
        assert review_data["created_at"] is not None

    def test_review_detail_returns_correct_data(self, api_client, review):
        url = reverse("reviews:api_review_detail", kwargs={"id": review.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["text"] == "Очень красивое и удобное худи"
        assert response.data["rating"] == 5
        assert response.data["user_username"] == "alice"
        assert response.data["created_at"] is not None

    def test_review_create_requires_auth(self, api_client, hoodie_product):
        url = reverse("reviews:api_review_create")
        payload = {
            "product": hoodie_product.id,
            "text": "Новый отзыв о худи",
            "rating": 4,
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code in (401, 403)

    def test_review_create_works_for_authenticated_user(self, api_client, user, hoodie_product):
        api_client.force_authenticate(user=user)
        url = reverse("reviews:api_review_create")
        payload = {
            "product": hoodie_product.id,
            "text": "Новый отзыв о худи",
            "rating": 4,
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 201
        assert Review.objects.filter(user=user, product=hoodie_product, text="Новый отзыв о худи").exists() is True

        created_review = Review.objects.get(user=user, product=hoodie_product, text="Новый отзыв о худи")
        assert created_review.rating == 4


@pytest.mark.django_db
class TestOrdersAPI:
    def test_order_list_requires_auth(self, api_client):
        url = reverse("orders:api_order_list")
        response = api_client.get(url)

        assert response.status_code in (401, 403)

    def test_order_list_returns_only_current_user_orders(self, api_client, user, another_user, order, another_user_order, mug_product):
        OrderItem.objects.create(
            order=order,
            product=mug_product,
            price=Decimal("400.00"),
            quantity=1
        )
        OrderItem.objects.create(
            order=another_user_order,
            product=mug_product,
            price=Decimal("400.00"),
            quantity=2
        )

        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 1

        order_data = response.data["results"][0]
        assert order_data["id"] == order.id
        assert order_data["user_username"] == "alice"

    def test_order_detail_returns_only_owner_order(self, api_client, user, order, earrings_product):
        OrderItem.objects.create(
            order=order,
            product=earrings_product,
            price=Decimal("1200.00"),
            quantity=2
        )

        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_detail", kwargs={"id": order.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == order.id
        assert response.data["user_username"] == "alice"
        assert response.data["items_count"] == 1
        assert len(response.data["items"]) == 1

    def test_order_detail_returns_404_for_foreign_order(self, api_client, user, another_user_order):
        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_detail", kwargs={"id": another_user_order.id})
        response = api_client.get(url)

        assert response.status_code == 404

    def test_order_create_requires_auth(self, api_client, mug_product):
        url = reverse("orders:api_order_create")
        payload = {
            "items": [
                {
                    "product": mug_product.id,
                    "quantity": 1
                }
            ]
        }

        response = api_client.post(url, payload, format="json")
        assert response.status_code in (401, 403)

    def test_order_create_creates_order_items_and_updates_stock(self, api_client, user, hoodie_product):
        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_create")
        payload = {
            "items": [
                {
                    "product": hoodie_product.id,
                    "quantity": 2
                }
            ]
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 201
        assert Order.objects.filter(user=user).count() == 1

        order = Order.objects.get(user=user)
        assert order.items.count() == 1

        item = order.items.first()
        assert item.product == hoodie_product
        assert item.quantity == 2
        assert item.price == Decimal("3500.00")

        hoodie_product.refresh_from_db()
        assert hoodie_product.stock == 8

        order.refresh_from_db()
        assert order.total_price == Decimal("7000.00")

    def test_order_create_fails_if_items_empty(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_create")
        payload = {
            "items": []
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 400
        assert "items" in response.data

    def test_order_create_fails_if_quantity_less_than_one(self, api_client, user, tshirt_product):
        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_create")
        payload = {
            "items": [
                {
                    "product": tshirt_product.id,
                    "quantity": 0
                }
            ]
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 400

    def test_order_create_fails_if_not_enough_stock(self, api_client, user, tshirt_product):
        api_client.force_authenticate(user=user)
        url = reverse("orders:api_order_create")
        payload = {
            "items": [
                {
                    "product": tshirt_product.id,
                    "quantity": 100
                }
            ]
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 400
        assert Order.objects.filter(user=user).count() == 0

    def test_order_all_list_is_public_in_current_implementation(self, api_client, order, mug_product):
        OrderItem.objects.create(
            order=order,
            product=mug_product,
            price=Decimal("400.00"),
            quantity=1
        )

        url = reverse("orders:api_order_all")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) >= 1