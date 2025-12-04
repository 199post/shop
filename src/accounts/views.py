from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from store.models import Order, Cart, Favorite


def register_view(request):
    """Представление для регистрации нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Акаунт створено для {username}!')
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
                messages.info(request, f'Ви увійшли як {username}.')
                # Перенаправляем на страницу, с которой пришел пользователь
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Невірне ім\'я користувача або пароль.')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    """Представление для просмотра и редактирования профиля пользователя"""
    
    if request.method == 'POST':
        # Обробка редагування профілю
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        
        try:
            user.save()
            messages.success(request, 'Профіль успішно оновлено!')
        except Exception as e:
            messages.error(request, f'Помилка при оновленні профілю: {str(e)}')
        
        return redirect('profile')
    
    # Получаем заказы пользователя
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')[:5]
    
    # Получаем количество товаров в корзине
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.get_total_items()

    # Избранные товары
    favorite_products = [f.product for f in Favorite.objects.filter(user=request.user).select_related("product", "product__category")]
    
    context = {
        'user': request.user,
        'orders': orders,
        'cart_items_count': cart_items_count,
        'favorite_products': favorite_products,
    }
    return render(request, 'accounts/profile.html', context)


def logout_view(request):
    """Представление для выхода пользователя"""
    logout(request)
    messages.success(request, 'Ви успішно вийшли з системи.')
    return redirect('index')


