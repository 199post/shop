from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def index(request):
    """Главная страница с последними товарами"""
    products = Product.objects.all()[:8]  # Последние 8 товаров
    categories = Category.objects.all()
    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories
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
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {
        'categories': categories
    })
