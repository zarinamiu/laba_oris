from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'rating': forms.Select(attrs={
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 200px;'
            }, choices=[
                (1, '⭐ - Ужасно'),
                (2, '⭐⭐ - Плохо'),
                (3, '⭐⭐⭐ - Нормально'),
                (4, '⭐⭐⭐⭐ - Хорошо'),
                (5, '⭐⭐⭐⭐⭐ - Отлично'),
            ])
        }
        
        labels = {
            'text': 'Ваш отзыв',
            'rating': 'Оценка'
        }
