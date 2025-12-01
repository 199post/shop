from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Product, Category, Cart, CartItem, Order, OrderItem

def index(request):
    """Главная страница с последними товарами"""
    products = Product.objects.all()[:8]  # Последние 8 товаров
    categories = Category.objects.all()
    
    # Получаем количество товаров в корзине для авторизованного пользователя
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
    
    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories,
        'cart_items_count': cart_items_count,
    })

def product_list(request):
    """Список всех товаров"""
    products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        selected_category = category
    else:
        selected_category = None
    
    # Получаем количество товаров в корзине
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'cart_items_count': cart_items_count,
    })

def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    
    # Получаем количество товаров в корзине
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_items_count': cart_items_count,
    })

def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.all()
    
    # Получаем количество товаров в корзине
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
    
    return render(request, 'store/category_list.html', {
        'categories': categories,
        'cart_items_count': cart_items_count,
    })


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Проверяем наличие товара
        if quantity > product.stock:
            messages.error(request, f'К сожалению, в наличии только {product.stock} шт.')
            return redirect('product_detail', product_id=product_id)
        
        # Получаем или создаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Добавляем или обновляем товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Если товар уже в корзине, увеличиваем количество
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f'К сожалению, в наличии только {product.stock} шт.')
                return redirect('product_detail', product_id=product_id)
            cart_item.quantity = new_quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} добавлен в корзину!')
        return redirect('cart_detail')
    
    return redirect('product_detail', product_id=product_id)


@login_required
def cart_detail(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    return render(request, 'store/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_items_count': cart.get_total_items(),
    })


@login_required
def update_cart_item(request, item_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Товар удален из корзины')
        elif quantity > cart_item.product.stock:
            messages.error(request, f'К сожалению, в наличии только {cart_item.product.stock} шт.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено')
    
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} удален из корзины')
    return redirect('cart_detail')


@login_required
@transaction.atomic
def checkout(request):
    """Оформление заказа"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart_detail')
    
    # Проверяем наличие товаров
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'Недостаточно товара {item.product.name} на складе')
            return redirect('cart_detail')
    
    # Создаем заказ
    total_price = cart.get_total_price()
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )
    
    # Создаем элементы заказа и уменьшаем количество товара на складе
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # Уменьшаем количество товара на складе
        item.product.stock -= item.quantity
        item.product.save()
    
    # Очищаем корзину
    cart_items.delete()
    
    messages.success(request, f'Заказ #{order.id} успешно оформлен! Дождитесь, с вами свяжется оператор.')
    return redirect('order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Получаем количество товаров в корзине
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.get_total_items()
    
    return render(request, 'store/order_detail.html', {
        'order': order,
        'cart_items_count': cart_items_count,
    })


@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    # Получаем количество товаров в корзине
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.get_total_items()
    
    return render(request, 'store/order_list.html', {
        'orders': orders,
        'cart_items_count': cart_items_count,
    })

