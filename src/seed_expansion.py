import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product

def seed_expansion():
    print("Starting expansion...")

    # 1. Expand Mobile Phones
    phones_cat, _ = Category.objects.get_or_create(name="Мобільні телефони", defaults={'slug': 'mobile-phones'})
    
    phone_brands = ["Samsung", "Apple", "Xiaomi", "Motorola", "Google"]
    for brand in phone_brands:
        slug = f"mobile-{brand.lower()}"
        sub, created = Category.objects.get_or_create(
            name=brand,
            parent=phones_cat,
            defaults={'slug': slug}
        )
        if created:
            print(f"Created subcategory: {brand}")

    # 2. Add 4 new categories
    new_categories = {
        "Ноутбуки": ["Asus", "Lenovo", "HP", "Acer", "Apple"],
        "Телевізори": ["Samsung", "LG", "Sony", "Philips"],
        "Смарт-годинники": ["Apple Watch", "Samsung Galaxy Watch", "Garmin", "Amazfit"],
        "Фотоапарати": ["Canon", "Nikon", "Sony", "Fujifilm"]
    }

    for cat_name, brands in new_categories.items():
        slug = cat_name.lower().replace(' ', '-')
        # Transliterate roughly if needed, but for now just simple replacement
        if cat_name == "Ноутбуки": slug = "laptops"
        elif cat_name == "Телевізори": slug = "tvs"
        elif cat_name == "Смарт-годинники": slug = "smartwatches"
        elif cat_name == "Фотоапарати": slug = "cameras"

        cat, created = Category.objects.get_or_create(name=cat_name, defaults={'slug': slug})
        if created:
            print(f"Created category: {cat_name}")
        
        for brand in brands:
            sub_slug = f"{slug}-{brand.lower().replace(' ', '-')}"
            sub, _ = Category.objects.get_or_create(
                name=brand,
                parent=cat,
                defaults={'slug': sub_slug}
            )

            # Add some products
            for i in range(3):
                product_name = f"{brand} {cat_name} Model {random.randint(100, 999)}"
                price = random.randint(5000, 50000)
                Product.objects.get_or_create(
                    name=product_name,
                    category=sub,
                    defaults={
                        'price': price,
                        'description': f"Чудовий {cat_name.lower()} від {brand}. Гарантія якості.",
                        'stock': random.randint(5, 50)
                    }
                )
    
    print("Expansion completed!")

if __name__ == '__main__':
    seed_expansion()
