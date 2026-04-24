from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from catalog.models import Product


@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_create(request):
    """Создание заказа из корзины"""
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, 'Корзина пуста!')
        return redirect('catalog:cart_view')

    if request.method == 'POST':
        # Создаём заказ
        order = Order.objects.create(user=request.user)

        # Добавляем товары из корзины
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=product_id, is_available=True)

                if product.stock >= quantity:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity
                    )
                    product.stock -= quantity
                    product.save()
            except Product.DoesNotExist:
                continue

        # Пересчитываем сумму
        order.calculate_total()

        # Очищаем корзину
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, f'Заказ #{order.id} успешно создан! ✅')
        return redirect('orders:order_detail', order_id=order.id)

    # GET запрос - показываем форму
    items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            total += item_total
            items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'orders/order_create.html', {
        'items': items,
        'total': total
    })


@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})