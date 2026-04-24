from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
            'placeholder': 'Введите email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
                'placeholder': 'Придумайте имя пользователя'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
            'placeholder': 'Повторите пароль'
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 12px; border: 2px solid #f8bbd9; border-radius: 8px; font-size: 16px; box-sizing: border-box;',
                'rows': 3,
                'placeholder': 'Введите адрес доставки'
            }),
        }
        
        labels = {
            'phone': '📱 Телефон',
            'address': '🏠 Адрес доставки'
        }
