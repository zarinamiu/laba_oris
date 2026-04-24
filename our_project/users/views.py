from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import CustomRegisterForm, ProfileForm


def user_login(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! 🎀')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')

    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы! 👋')
    return redirect('home')


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать в PinkStore! 🌸')
            return redirect('users:profile')
    else:
        form = CustomRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль пользователя"""
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные профиля успешно обновлены! ✅')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user_profile)

    context = {
        'profile': user_profile,
        'form': form
    }
    return render(request, 'users/profile.html', context)