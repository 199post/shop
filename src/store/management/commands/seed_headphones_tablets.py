from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed headphones and tablets with subcategories (brands)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories and products...')
        
        # Створюємо категорію Навушники
        headphones_cat, created = Category.objects.get_or_create(
            name='Навушники',
            slug='navushnyky',
            defaults={'parent': None}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {headphones_cat.name}'))
        
        # Підкатегорії для навушників (бренди)
        headphone_brands = [
            ('Koss', 'koss-headphones'),
            ('Samsung', 'samsung-headphones'),
            ('Realme', 'realme-headphones'),
            ('AirPods', 'airpods'),
            ('Soundcore', 'soundcore-headphones'),
        ]
        
        headphone_subcats = {}
        for brand_name, brand_slug in headphone_brands:
            subcat, created = Category.objects.get_or_create(
                name=brand_name,
                slug=brand_slug,
                defaults={'parent': headphones_cat}
            )
            headphone_subcats[brand_name] = subcat
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created subcategory: {brand_name}'))
        
        # Створюємо 40 навушників (по ~8 для кожного бренду)
        headphone_models = {
            'Koss': [
                ('Koss PortaPro', 1200, 1500),
                ('Koss KPH30i', 800, 1000),
                ('Koss Sporta Pro', 1500, 1800),
                ('Koss KSC75', 600, 800),
                ('Koss UR20', 900, 1100),
                ('Koss BT540i', 2500, 3000),
                ('Koss GMR-545', 2000, 2500),
                ('Koss QZ99', 4000, 5000),
            ],
            'Samsung': [
                ('Samsung Galaxy Buds 2 Pro', 4500, 6000),
                ('Samsung Galaxy Buds FE', 2800, 3500),
                ('Samsung Galaxy Buds Live', 3200, 4000),
                ('Samsung Galaxy Buds 2', 3000, 3800),
                ('Samsung AKG N700NC M2', 7000, 9000),
                ('Samsung Level On Wireless', 2500, 3200),
                ('Samsung Gear IconX', 3500, 4500),
                ('Samsung Level U Pro', 1800, 2300),
            ],
            'Realme': [
                ('Realme Buds Air 5 Pro', 2200, 2800),
                ('Realme Buds Air 3', 1500, 2000),
                ('Realme Buds T300', 1800, 2300),
                ('Realme Buds Q2', 900, 1200),
                ('Realme Buds Wireless 2 Neo', 800, 1000),
                ('Realme Buds Air Pro', 2000, 2500),
                ('Realme TechLife Buds T100', 600, 800),
                ('Realme Buds Air 2', 1200, 1500),
            ],
            'AirPods': [
                ('Apple AirPods Pro 2', 9000, 11000),
                ('Apple AirPods 3', 6000, 7500),
                ('Apple AirPods 2', 4500, 5500),
                ('Apple AirPods Max', 19000, 23000),
                ('Apple Beats Studio Buds', 4500, 5500),
                ('Apple Beats Fit Pro', 5500, 6500),
                ('Apple Beats Solo 3', 6000, 7500),
                ('Apple Beats Studio 3', 10000, 12000),
            ],
            'Soundcore': [
                ('Soundcore Liberty 4 NC', 3200, 4000),
                ('Soundcore Space A40', 2500, 3200),
                ('Soundcore Life P3', 1800, 2300),
                ('Soundcore Liberty 3 Pro', 4500, 5500),
                ('Soundcore Life Q30', 2800, 3500),
                ('Soundcore Life Q20', 1800, 2300),
                ('Soundcore Liberty Air 2 Pro', 3500, 4200),
                ('Soundcore Space Q45', 4000, 5000),
            ],
        }
        
        headphones_count = 0
        for brand, models in headphone_models.items():
            for model_name, price_min, price_max in models:
                price = random.randint(price_min, price_max)
                stock = random.randint(5, 50)
                
                product, created = Product.objects.get_or_create(
                    name=model_name,
                    category=headphone_subcats[brand],
                    defaults={
                        'price': Decimal(str(price)),
                        'stock': stock,
                        'description': f'Високоякісні навушники {model_name}. Відмінний звук та комфорт.',
                    }
                )
                if created:
                    headphones_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {headphones_count} headphones'))
        
        # Створюємо категорію Планшети
        tablets_cat, created = Category.objects.get_or_create(
            name='Планшети',
            slug='planshety',
            defaults={'parent': None}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {tablets_cat.name}'))
        
        # Підкатегорії для планшетів (бренди)
        tablet_brands = [
            ('Samsung', 'samsung-tablets'),
            ('Xiaomi', 'xiaomi-tablets'),
            ('Apple', 'apple-tablets'),
            ('Lenovo', 'lenovo-tablets'),
            ('Huawei', 'huawei-tablets'),
        ]
        
        tablet_subcats = {}
        for brand_name, brand_slug in tablet_brands:
            subcat, created = Category.objects.get_or_create(
                name=brand_name,
                slug=brand_slug,
                defaults={'parent': tablets_cat}
            )
            tablet_subcats[brand_name] = subcat
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created subcategory: {brand_name}'))
        
        # Створюємо 100 планшетів
        tablet_models = {
            'Samsung': [
                ('Samsung Galaxy Tab S9 Ultra', 35000, 42000),
                ('Samsung Galaxy Tab S9+', 28000, 34000),
                ('Samsung Galaxy Tab S9', 24000, 30000),
                ('Samsung Galaxy Tab S8 Ultra', 30000, 36000),
                ('Samsung Galaxy Tab S8+', 24000, 29000),
                ('Samsung Galaxy Tab S8', 20000, 25000),
                ('Samsung Galaxy Tab S7 FE', 15000, 18000),
                ('Samsung Galaxy Tab S6 Lite', 9000, 12000),
                ('Samsung Galaxy Tab A9+', 7000, 9000),
                ('Samsung Galaxy Tab A9', 5000, 7000),
                ('Samsung Galaxy Tab A8', 6000, 8000),
                ('Samsung Galaxy Tab A7 Lite', 4500, 6000),
                ('Samsung Galaxy Tab Active 4 Pro', 28000, 35000),
                ('Samsung Galaxy Tab S9 FE', 13000, 16000),
                ('Samsung Galaxy Tab S9 FE+', 16000, 19000),
                ('Samsung Galaxy Tab S7', 18000, 22000),
                ('Samsung Galaxy Tab S7+', 25000, 30000),
                ('Samsung Galaxy Tab S6', 15000, 19000),
                ('Samsung Galaxy Tab A 10.1', 5500, 7500),
                ('Samsung Galaxy Tab Active 3', 15000, 18000),
            ],
            'Xiaomi': [
                ('Xiaomi Pad 6 Pro', 15000, 18000),
                ('Xiaomi Pad 6', 12000, 15000),
                ('Xiaomi Pad 5 Pro', 13000, 16000),
                ('Xiaomi Pad 5', 10000, 13000),
                ('Xiaomi Redmi Pad Pro', 9000, 11000),
                ('Xiaomi Redmi Pad SE', 6000, 8000),
                ('Xiaomi Redmi Pad', 7000, 9000),
                ('Xiaomi Mi Pad 5', 11000, 14000),
                ('Xiaomi Pad 6 Max 14', 24000, 28000),
                ('Xiaomi Poco Pad', 8000, 10000),
                ('Xiaomi Pad SE', 5000, 7000),
                ('Xiaomi Mi Pad 4', 6000, 8000),
                ('Xiaomi Mi Pad 4 Plus', 7500, 9500),
                ('Xiaomi Redmi Pad 10', 6500, 8500),
                ('Xiaomiабл Pad 6S Pro', 17000, 20000),
                ('Xiaomi Pad Air', 13000, 16000),
                ('Xiaomi Mi Pad 3', 5000, 6500),
                ('Xiaomi Redmi Tab', 4500, 6000),
                ('Xiaomi Pad Mini', 8000, 10000),
                ('Xiaomi Note Pad', 10000, 12000),
            ],
            'Apple': [
                ('Apple iPad Pro 12.9" M2', 45000, 55000),
                ('Apple iPad Pro 11" M2', 35000, 42000),
                ('Apple iPad Air M2', 25000, 30000),
                ('Apple iPad 10th gen', 15000, 18000),
                ('Apple iPad Mini 6', 18000, 22000),
                ('Apple iPad Pro 12.9" M1', 40000, 48000),
                ('Apple iPad Pro 11" M1', 32000, 38000),
                ('Apple iPad Air 5', 22000, 27000),
                ('Apple iPad Air 4', 18000, 23000),
                ('Apple iPad 9th gen', 12000, 15000),
                ('Apple iPad Mini 5', 14000, 17000),
                ('Apple iPad 8th gen', 11000, 14000),
                ('Apple iPad Pro 12.9" 2021', 38000, 45000),
                ('Apple iPad Pro 11" 2021', 30000, 36000),
                ('Apple iPad Pro 12.9" 2020', 35000, 42000),
                ('Apple iPad Pro 11" 2020', 28000, 34000),
                ('Apple iPad Air 3', 15000, 19000),
                ('Apple iPad 7th gen', 10000, 13000),
                ('Apple iPad Mini 4', 11000, 14000),
                ('Apple iPad Pro 10.5"', 20000, 25000),
            ],
            'Lenovo': [
                ('Lenovo Tab P12', 14000, 17000),
                ('Lenovo Tab P11 Pro Gen 2', 13000, 16000),
                ('Lenovo Tab P11 Plus', 9000, 11000),
                ('Lenovo Tab M10 Plus 3rd Gen', 6000, 8000),
                ('Lenovo Tab M10 FHD Plus', 5000, 7000),
                ('Lenovo Tab M8 4th Gen', 3500, 5000),
                ('Lenovo Yoga Tab 13', 25000, 30000),
                ('Lenovo Yoga Tab 11', 15000, 18000),
                ('Lenovo Tab P11', 8000, 10000),
                ('Lenovo Tab M10 HD', 4000, 5500),
                ('Lenovo Tab K10', 8000, 10000),
                ('Lenovo Tab M7', 2500, 3500),
                ('Lenovo Smart Tab M10', 6000, 8000),
                ('Lenovo Yoga Smart Tab', 9000, 11000),
                ('Lenovo Tab 4 10 Plus', 7000, 9000),
                ('Lenovo Tab P10', 7500, 9500),
                ('Lenovo Tab E10', 4000, 5500),
                ('Lenovo Tab E8', 3000, 4000),
                ('Lenovo Tab M7 Gen 3', 2800, 3800),
                ('Lenovo Tab M8 HD', 3500, 4500),
            ],
            'Huawei': [
                ('Huawei MatePad Pro 13.2', 28000, 34000),
                ('Huawei MatePad Pro 12.6', 25000, 30000),
                ('Huawei MatePad Pro 11', 18000, 22000),
                ('Huawei MatePad 11.5', 12000, 15000),
                ('Huawei MatePad SE', 6000, 8000),
                ('Huawei MatePad 10.4', 8000, 10000),
                ('Huawei MediaPad M6', 12000, 15000),
                ('Huawei MediaPad M5 Lite', 8000, 10000),
                ('Huawei MediaPad T5', 5500, 7000),
                ('Huawei MediaPad T3', 3500, 4500),
                ('Huawei MatePad Paper', 15000, 18000),
                ('Huawei MatePad T10s', 5000, 6500),
                ('Huawei MatePad T8', 3000, 4000),
                ('Huawei MediaPad M5 Pro', 14000, 17000),
                ('Huawei MediaPad M5 10', 11000, 14000),
                ('Huawei MediaPad M5 8', 9000, 11000),
                ('Huawei MediaPad M3 Lite', 6000, 8000),
                ('Huawei Media Pad M2', 5000, 6500),
                ('Huawei MatePad 10.8', 14000, 17000),
                ('Huawei MatePad Matepad', 9000, 11000),
            ],
        }
        
        tablets_count = 0
        for brand, models in tablet_models.items():
            for model_name, price_min, price_max in models:
                price = random.randint(price_min, price_max)
                stock = random.randint(3, 40)
                
                # Випадкова знижка для деяких товарів
                has_discount = random.random() < 0.3  # 30% ймовірність знижки
                sale_price = None
                if has_discount:
                    discount_percent = random.randint(10, 30)
                    sale_price = price * (100 - discount_percent) / 100
                
                product, created = Product.objects.get_or_create(
                    name=model_name,
                    category=tablet_subcats[brand],
                    defaults={
                        'price': Decimal(str(price)),
                        'sale_price': Decimal(str(int(sale_price))) if sale_price else None,
                        'stock': stock,
                        'description': f'Потужний планшет {model_name}. Ідеальний для роботи та розваг.',
                    }
                )
                if created:
                    tablets_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {tablets_count} tablets'))
        self.stdout.write(self.style.SUCCESS(f'\nTotal: {headphones_count + tablets_count} products created'))
