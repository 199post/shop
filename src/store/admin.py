from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Favorite, Page, FooterSection, FooterLink, ProductImage


class SubCategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    extra = 1
    verbose_name = "Подкатегория"
    verbose_name_plural = "Подкатегории"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent"]
    list_filter = ["parent"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "image_preview", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["image_preview"]
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"

    image_preview.short_description = "Превью"
    image_preview.allow_tags = True


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'updated_at']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'get_total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Если статус изменился на "В обработке", можно отправить уведомление
        if change and 'status' in form.changed_data:
            # Здесь можно добавить логику отправки email
            pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "user__email", "product__name"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "content"]


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    inlines = [FooterLinkInline]
    ordering = ["order"]
