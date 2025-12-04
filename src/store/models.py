from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Категория товара.
    Поддерживает подкатегории через поле parent:
    - parent = NULL  -> корневая категория (например, "Мобильные телефоны")
    - parent != NULL -> подкатегория (например, "Apple", "Samsung" и т.п.)
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
        verbose_name="Родительская категория",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    @property
    def is_root(self) -> bool:
        """Является ли категория корневой (без родителя)."""
        return self.parent is None

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Акционная цена",
        help_text="Оставьте пустым, если товара нет на скидке",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    # Main image (optional, for backward compatibility or as a thumbnail)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Фото товара",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self):
        return self.name

    def has_discount(self):
        """Есть ли активная скидка."""
        return self.sale_price is not None and self.sale_price < self.price

    def get_discount_percentage(self):
        """Процент скидки для бейджа."""
        if self.has_discount():
            discount = ((self.price - self.sale_price) / self.price) * 100
            return int(discount)
        return 0

    def get_effective_price(self):
        """Фактическая цена (учитывая скидку)."""
        return self.sale_price if self.has_discount() else self.price

class ProductImage(models.Model):
    """
    Дополнительные изображения товара.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина {self.user.username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.price * self.quantity


class Favorite(models.Model):
    """
    Избранные товары пользователя.
    Один товар может быть в избранном у многих пользователей,
    один пользователь может иметь много избранных товаров.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites", verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorite_for", verbose_name="Товар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"


class Page(models.Model):
    """
    Статичні сторінки (Про нас, Доставка, Контакти тощо).
    """
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL (slug)")
    content = models.TextField(verbose_name="Вміст (HTML)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сторінка"
        verbose_name_plural = "Сторінки"

    def __str__(self):
        return self.title


class FooterSection(models.Model):
    """
    Розділ футера (наприклад, "Інформація про компанію", "Допомога").
    """
    title = models.CharField(max_length=100, verbose_name="Заголовок розділу")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")

    class Meta:
        ordering = ['order']
        verbose_name = "Розділ футера"
        verbose_name_plural = "Розділи футера"

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    """
    Посилання у футері.
    """
    section = models.ForeignKey(FooterSection, related_name='links', on_delete=models.CASCADE, verbose_name="Розділ")
    title = models.CharField(max_length=100, verbose_name="Текст посилання")
    url = models.CharField(max_length=200, verbose_name="URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")

    class Meta:
        ordering = ['order']
        verbose_name = "Посилання футера"
        verbose_name_plural = "Посилання футера"

    def __str__(self):
        return f"{self.section.title} -> {self.title}"