from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Review
from .forms import ReviewForm
from catalog.models import Product


@login_required
def add_review(request, product_id):
    """Создание нового отзыва"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен! ✅')
            return redirect('catalog:product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})


@login_required
def edit_review(request, review_id):
    """Редактирование отзыва (с защитой от IDOR)"""
    review = get_object_or_404(Review, id=review_id)
    
    # ЗАЩИТА ОТ IDOR
    if review.user != request.user:
        return HttpResponseForbidden("У вас нет прав на редактирование этого отзыва!")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлён! ✅')
            return redirect('catalog:product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    """Удаление отзыва (с защитой от IDOR)"""
    review = get_object_or_404(Review, id=review_id)
    
    # ЗАЩИТА ОТ IDOR
    if review.user != request.user:
        return HttpResponseForbidden("У вас нет прав на удаление этого отзыва!")
    
    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, 'Отзыв успешно удалён! 🗑️')
        return redirect('catalog:product_detail', product_id=product_id)
    
    return render(request, 'reviews/confirm_delete.html', {'review': review})


def review_list(request):
    """Список всех отзывов"""
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})
