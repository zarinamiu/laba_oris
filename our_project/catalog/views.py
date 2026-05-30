from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Category, Product


def home(request):
    """Главная страница"""
    products = Product.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    return render(request, 'catalog/home.html', {
        'products': products,
        'categories': categories
    })


def product_list(request, category_slug=None):
    """Каталог товаров"""
    products = Product.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.all()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category
    })


def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().select_related('user')

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'reviews': reviews
    })


def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id)

    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session.modified = True

    messages.success(request, f'🌸 {product.title} добавлен в корзину!')
    return redirect(request.META.get('HTTP_REFERER', 'catalog:product_list'))


def cart_view(request):
    """Просмотр корзины"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            if product_id_str in request.session.get('cart', {}):
                del request.session['cart'][product_id_str]
                request.session.modified = True

    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(cart.values()),
    })


def remove_from_cart(request, product_id):
    """Удаление товара из корзины"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session.modified = True
        messages.success(request, 'Товар удалён из корзины')

    return redirect('catalog:cart_view')


def update_cart(request, product_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if quantity > 0:
            cart[product_id_str] = quantity
        else:
            cart.pop(product_id_str, None)

        request.session.modified = True

    return redirect('catalog:cart_view')


def toggle_theme(request):
    current_theme = request.COOKIES.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'

    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('theme', new_theme, max_age=31536000, path='/')

    return response


@login_required
def chat_room(request, room_name):
    return render(request, 'catalog/chat.html', {
        'room_name': room_name
    })