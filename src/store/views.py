from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction, models
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Favorite, Page


def _apply_filters_and_sorting(request, qs):
    """
    Общая логика фильтрации и сортировки товаров.
    Поддерживает:
    - ?min_price=...
    - ?max_price=...
    - ?sort=popular|price_asc|price_desc|new
    """
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "popular")
    query = request.GET.get("q")

    if query:
        qs = qs.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))

    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)

    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-created_at")
    else:
        # popular – пока сортируем по дате создания (можно расширить метрикой продаж/просмотров)
        qs = qs.order_by("-created_at")

    return qs


def index(request):
    """Главная страница с товарами, фильтрами и сортировкой."""
    products = Product.objects.all()

    # Фильтр по категории и подкатегории
    category_slug = request.GET.get("category")
    subcategory_slug = request.GET.get("subcategory")
    selected_category = None
    selected_subcategory = None

    root_categories = Category.objects.filter(parent__isnull=True)

    if category_slug:
        selected_category = get_object_or_404(
            Category, slug=category_slug, parent__isnull=True
        )
        products = products.filter(
            category__in=Category.objects.filter(
                models.Q(id=selected_category.id) | models.Q(parent=selected_category)
            )
        )

        if subcategory_slug:
            selected_subcategory = get_object_or_404(
                Category, slug=subcategory_slug, parent=selected_category
            )
            products = products.filter(category=selected_subcategory)

    products = _apply_filters_and_sorting(request, products)

    # Применяем сортировку/фильтры
    products = _apply_filters_and_sorting(request, products)

    # Показываем только первые 12 товаров на главной
    products = products[:12]

    # Получаем количество товаров в корзине и избранное для авторизованного пользователя
    cart_items_count = 0
    favorite_ids = set()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
        favorite_ids = set(
            Favorite.objects.filter(user=request.user, product__in=products).values_list(
                "product_id", flat=True
            )
        )

    context = {
        "products": products,
        "root_categories": root_categories,
        "selected_category": selected_category,
        "selected_subcategory": selected_subcategory,
        "cart_items_count": cart_items_count,
        "favorite_ids": favorite_ids,
        "current_sort": request.GET.get("sort", "popular"),
        "min_price": request.GET.get("min_price", ""),
        "min_price": request.GET.get("min_price", ""),
        "max_price": request.GET.get("max_price", ""),
        "query": request.GET.get("q", ""),
    }
    return render(request, "store/index.html", context)


def product_list(request):
    """Список всех товаров с фильтрами, категориями и подкатегориями."""
    products = Product.objects.all()
    root_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    category_slug = request.GET.get("category")
    subcategory_slug = request.GET.get("subcategory")
    selected_category = None
    selected_subcategory = None

    if category_slug:
        selected_category = get_object_or_404(
            Category, slug=category_slug, parent__isnull=True
        )
        products = products.filter(
            category__in=Category.objects.filter(
                models.Q(id=selected_category.id) | models.Q(parent=selected_category)
            )
        )

        if subcategory_slug:
            selected_subcategory = get_object_or_404(
                Category, slug=subcategory_slug, parent=selected_category
            )
            products = products.filter(category=selected_subcategory)

    products = _apply_filters_and_sorting(request, products)

    # Получаем количество товаров в корзине и избранное
    cart_items_count = 0
    favorite_ids = set()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
        favorite_ids = set(
            Favorite.objects.filter(user=request.user, product__in=products).values_list(
                "product_id", flat=True
            )
        )

    context = {
        "products": products,
        "root_categories": root_categories,
        "selected_category": selected_category,
        "selected_subcategory": selected_subcategory,
        "cart_items_count": cart_items_count,
        "favorite_ids": favorite_ids,
        "current_sort": request.GET.get("sort", "popular"),
        "min_price": request.GET.get("min_price", ""),
        "max_price": request.GET.get("max_price", ""),
        "query": request.GET.get("q", ""),
        "min_price": request.GET.get("min_price", ""),
        "max_price": request.GET.get("max_price", ""),
    }
    return render(request, "store/product_list.html", context)

def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    
    # Получаем количество товаров в корзине и статус избранного
    cart_items_count = 0
    is_favorite = False
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_items_count': cart_items_count,
        'is_favorite': is_favorite,
    })

def category_list(request):
    """Список корневых категорий и их подкатегорий."""
    root_categories = Category.objects.filter(parent__isnull=True).prefetch_related(
        "subcategories", "products"
    )

    # Получаем количество товаров в корзине
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()

    return render(
        request,
        "store/category_list.html",
        {
            "categories": root_categories,
            "cart_items_count": cart_items_count,
        },
    )


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


@login_required
def favorites_list(request):
    """Список избранных товаров пользователя."""
    favorites = Favorite.objects.filter(user=request.user).select_related("product", "product__category")
    products = [fav.product for fav in favorites]

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.get_total_items()

    return render(
        request,
        "store/favorites_list.html",
        {
            "products": products,
            "cart_items_count": cart_items_count,
        },
    )


@login_required
def toggle_favorite(request, product_id):
    """
    Переключение избранного для товара.
    Ожидает POST-запрос. После изменения возвращает пользователя назад.
    """
    product = get_object_or_404(Product, id=product_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        messages.info(request, f"{product.name} удалён из избранного.")
    else:
        messages.success(request, f"{product.name} добавлен в избранное.")

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or redirect("product_detail", product_id=product.id).url
    return redirect(next_url)


def search_suggestions(request):
    """API endpoint для автодоповнення пошуку."""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    # Шукаємо товари за назвою
    products = Product.objects.filter(
        name__icontains=query
    ).values('id', 'name', 'price')[:10]
    
    results = [
        {
            'id': p['id'],
            'name': p['name'],
            'price': float(p['price'])
        }
        for p in products
    ]
    
    return JsonResponse({'results': results})

def page_detail(request, slug):
    """Відображення статичної сторінки."""
    page = get_object_or_404(Page, slug=slug)
    
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.get_total_items()
        
    return render(request, 'store/page_detail.html', {
        'page': page,
        'cart_items_count': cart_items_count
    })
