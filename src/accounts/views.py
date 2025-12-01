from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from store.models import Order, Cart


def register_view(request):
    """Представление для регистрации нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Представление для входа пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Вы вошли как {username}.')
                # Перенаправляем на страницу, с которой пришел пользователь
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    """Представление для просмотра профиля пользователя"""
    # Получаем заказы пользователя
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')[:5]
    
    # Получаем количество товаров в корзине
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.get_total_items()
    
    context = {
        'user': request.user,
        'orders': orders,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'accounts/profile.html', context)


def logout_view(request):
    """Представление для выхода пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')


