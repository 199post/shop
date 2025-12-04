from decimal import Decimal
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import models

from store.models import Category, Product


class Command(BaseCommand):
    help = "Seeds the database with mobile phone data (120+ models with real UAH prices)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before seeding',
        )

    def handle(self, *args, **kwargs):
        clear_products = kwargs.get('clear', False)

        # Clear existing products if flag is set
        if clear_products:
            product_count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"Deleted {product_count} existing products"
            ))
        elif Product.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Products already exist. Use --clear flag to remove old products."
            ))
            return

        self.stdout.write(self.style.WARNING("Seeding mobile phone database..."))

        # ===================== USERS =====================
        self.stdout.write("Creating users...")
        
        # Create admin user if doesn't exist
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin/admin"))

        # ===================== CATEGORY =====================
        self.stdout.write("Creating category...")
        
        # Delete old categories (anything not mobile phones)
        old_categories = Category.objects.exclude(slug='mobile-phones')
        if old_categories.exists():
            old_count = old_categories.count()
            old_categories.delete()
            self.stdout.write(self.style.WARNING(f"Deleted {old_count} old categories"))
        
        phone_category, created = Category.objects.get_or_create(
            slug="mobile-phones",
            defaults={"name": "Мобільні телефони"},
        )
        if created:
            self.stdout.write(f"  Created category: Мобільні телефони")

        # ===================== MOBILE PHONES =====================
        self.stdout.write("Creating mobile phone products with real prices (UAH)...")

        # Real phone data with actual Ukrainian market prices
        phones = [
            # Samsung Galaxy S24 Series
            ("Samsung Galaxy S24 8GB/128GB", "Флагман 2024. AMOLED 6.2\" 120Hz, Snapdragon 8 Gen 3, камера 50MP, батарея 4000mAh", Decimal("37999"), 25),
            ("Samsung Galaxy S24 8GB/256GB", "Флагман 2024. AMOLED 6.2\" 120Hz, Snapdragon 8 Gen 3, камера 50MP, батарея 4000mAh", Decimal("39999"), 20),
            ("Samsung Galaxy S24 Plus 12GB/256GB", "Флагман 2024. AMOLED 6.7\" 120Hz, Snapdragon 8 Gen 3, камера 50MP, батарея 4900mAh", Decimal("47999"), 15),
            ("Samsung Galaxy S24 Ultra 12GB/256GB", "Топовий флагман. AMOLED 6.8\" 120Hz, Snapdragon 8 Gen 3, камера 200MP, S Pen, батарея 5000mAh", Decimal("57999"), 12),
            ("Samsung Galaxy S24 Ultra 12GB/512GB", "Топовий флагман. AMOLED 6.8\" 120Hz, Snapdragon 8 Gen 3, камера 200MP, S Pen, батарея 5000mAh", Decimal("61999"), 10),
            ("Samsung Galaxy S24 Ultra 12GB/1TB", "Топовий флагман. AMOLED 6.8\" 120Hz, Snapdragon 8 Gen 3, камера 200MP, S Pen, батарея 5000mAh", Decimal("71999"), 8),

            # Samsung Galaxy S23 Series
            ("Samsung Galaxy S23 8GB/128GB", "Флагман 2023. AMOLED 6.1\" 120Hz, Snapdragon 8 Gen 2, камера 50MP, батарея 3900mAh", Decimal("21192"), 30),
            ("Samsung Galaxy S23 8GB/256GB", "Флагман 2023. AMOLED 6.1\" 120Hz, Snapdragon 8 Gen 2, камера 50MP, батарея 3900mAh", Decimal("23385"), 25),
            ("Samsung Galaxy S23 Plus 8GB/256GB", "Флагман 2023. AMOLED 6.6\" 120Hz, Snapdragon 8 Gen 2, камера 50MP, батарея 4700mAh", Decimal("32999"), 18),
            ("Samsung Galaxy S23 Ultra 12GB/256GB", "Преміум флагман. AMOLED 6.8\" 120Hz, Snapdragon 8 Gen 2, камера 200MP, S Pen", Decimal("44603"), 15),

            # Samsung Galaxy Z Fold/Flip Series
            ("Samsung Galaxy Z Fold 5 12GB/256GB", "Складний флагман. 7.6\" Foldable AMOLED, Snapdragon 8 Gen 2, камера 50MP", Decimal("66923"), 8),
            ("Samsung Galaxy Z Fold 5 12GB/512GB", "Складний флагман. 7.6\" Foldable AMOLED, Snapdragon 8 Gen 2, камера 50MP", Decimal("72999"), 6),
            ("Samsung Galaxy Z Flip 5 8GB/256GB", "Компактний складний. 6.7\" Foldable AMOLED, Snapdragon 8 Gen 2, камера 12MP", Decimal("42999"), 12),
            ("Samsung Galaxy Z Flip 5 8GB/512GB", "Компактний складний. 6.7\" Foldable AMOLED, Snapdragon 8 Gen 2, камера 12MP", Decimal("46999"), 10),

            # Samsung Galaxy A Series
            ("Samsung Galaxy A54 5G 6GB/128GB", "Середній клас. Super AMOLED 6.4\" 120Hz, Exynos 1380, камера 50MP, IP67, батарея 5000mAh", Decimal("16599"), 40),
            ("Samsung Galaxy A54 5G 8GB/256GB", "Середній клас. Super AMOLED 6.4\" 120Hz, Exynos 1380, камера 50MP, IP67, батарея 5000mAh", Decimal("18999"), 35),
            ("Samsung Galaxy A34 5G 6GB/128GB", "Доступний 5G. Super AMOLED 6.6\" 120Hz, Dimensity 1080, камера 48MP, батарея 5000mAh", Decimal("7761"), 50),
            ("Samsung Galaxy A34 5G 8GB/256GB", "Доступний 5G. Super AMOLED 6.6\" 120Hz, Dimensity 1080, камера 48MP, батарея 5000mAh", Decimal("9151"), 45),
            ("Samsung Galaxy A24 6GB/128GB", "Бюджетний. 6.5\" Super AMOLED 90Hz, Helio G99, камера 50MP, батарея 5000mAh", Decimal("8999"), 50),
            ("Samsung Galaxy A14 5G 4GB/64GB", "Доступний 5G. 6.6\" IPS 90Hz, Dimensity 700, камера 50MP, батарея 5000mAh", Decimal("5499"), 65),
            ("Samsung Galaxy A04 3GB/64GB", "Ультра-бюджет. 6.5\" IPS, Helio P35, камера 50MP, батарея 5000mAh", Decimal("3299"), 75),

            # iPhone 16 Series
            ("iPhone 16 128GB", "Новинка 2024. 6.1\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 22 год", Decimal("47499"), 20),
            ("iPhone 16 256GB", "Новинка 2024. 6.1\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 22 год", Decimal("52499"), 18),
            ("iPhone 16 512GB", "Новинка 2024. 6.1\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 22 год", Decimal("62499"), 12),
            ("iPhone 16 Plus 128GB", "Новинка 2024. 6.7\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 26 год", Decimal("52499"), 15),
            ("iPhone 16 Plus 256GB", "Новинка 2024. 6.7\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 26 год", Decimal("57499"), 12),
            ("iPhone 16 Plus 512GB", "Новинка 2024. 6.7\" Super Retina XDR, A18 Bionic, камера 48MP, батарея до 26 год", Decimal("67499"), 10),
            ("iPhone 16 Pro 128GB", "Pro-серія 2024. 6.3\" ProMotion, A18 Pro, камера 48MP, Titanium, ProRAW/ProRes", Decimal("59499"), 15),
            ("iPhone 16 Pro 256GB", "Pro-серія 2024. 6.3\" ProMotion, A18 Pro, камера 48MP, Titanium, ProRAW/ProRes", Decimal("64999"), 12),
            ("iPhone 16 Pro 512GB", "Pro-серія 2024. 6.3\" ProMotion, A18 Pro, камера 48MP, Titanium, ProRAW/ProRes", Decimal("74999"), 8),
            ("iPhone 16 Pro 1TB", "Pro-серія 2024. 6.3\" ProMotion, A18 Pro, камера 48MP, Titanium, ProRAW/ProRes", Decimal("94999"), 5),
            ("iPhone 16 Pro Max 256GB", "Максимум від Apple. 6.9\" ProMotion, A18 Pro, камера 48MP телеоб'єктив 5x, Titanium", Decimal("70999"), 10),
            ("iPhone 16 Pro Max 512GB", "Максимум від Apple. 6.9\" ProMotion, A18 Pro, камера 48MP телеоб'єктив 5x, Titanium", Decimal("80999"), 8),
            ("iPhone 16 Pro Max 1TB", "Максимум від Apple. 6.9\" ProMotion, A18 Pro, камера 48MP телеоб'єктив 5x, Titanium", Decimal("90999"), 5),

            # iPhone 15 Series
            ("iPhone 15 128GB", "Флагман 2023. 6.1\" Super Retina XDR, A16 Bionic, камера 48MP, Dynamic Island", Decimal("40000"), 25),
            ("iPhone 15 256GB", "Флагман 2023. 6.1\" Super Retina XDR, A16 Bionic, камера 48MP, Dynamic Island", Decimal("45000"), 20),
            ("iPhone 15 512GB", "Флагман 2023. 6.1\" Super Retina XDR, A16 Bionic, камера 48MP, Dynamic Island", Decimal("48280"), 15),
            ("iPhone 15 Plus 128GB", "Великий екран. 6.7\" Super Retina XDR, A16 Bionic, камера 48MP, батарея до 26 год", Decimal("49999"), 18),
            ("iPhone 15 Plus 256GB", "Великий екран. 6.7\" Super Retina XDR, A16 Bionic, камера 48MP, батарея до 26 год", Decimal("54999"), 15),
            ("iPhone 15 Pro 128GB", "Pro 2023. 6.1\" ProMotion Titanium, A17 Pro, камера 48MP, Action Button", Decimal("54999"), 12),
            ("iPhone 15 Pro 256GB", "Pro 2023. 6.1\" ProMotion Titanium, A17 Pro, камера 48MP, Action Button", Decimal("59999"), 10),
            ("iPhone 15 Pro Max 256GB", "Топ 2023. 6.7\" ProMotion, A17 Pro, камера 48MP телеоб'єктив 5x, Titanium", Decimal("64999"), 8),
            ("iPhone 15 Pro Max 512GB", "Топ 2023. 6.7\" ProMotion, A17 Pro, камера 48MP телеоб'єктив 5x, Titanium", Decimal("72999"), 6),

            # iPhone 14 Series
            ("iPhone 14 128GB", "Популярна модель. 6.1\" Super Retina XDR, A15 Bionic, камера 12MP", Decimal("24480"), 35),
            ("iPhone 14 256GB", "Популярна модель. 6.1\" Super Retina XDR, A15 Bionic, камера 12MP", Decimal("26520"), 30),
            ("iPhone 14 Plus 128GB", "Великий дисплей. 6.7\" Super Retina XDR, A15 Bionic, камера 12MP, батарея до 26 год", Decimal("29999"), 25),
            ("iPhone 14 Pro 128GB", "Pro 2022. 6.1\" ProMotion, A16 Bionic, камера 48MP, Dynamic Island", Decimal("42999"), 15),
            ("iPhone 14 Pro Max 256GB", "Максимум 2022. 6.7\" ProMotion, A16 Bionic, камера 48MP, батарея до 29 год", Decimal("54999"), 10),

            # Xiaomi 14 Series
            ("Xiaomi 14 12GB/256GB", "Флагман 2024. 6.36\" AMOLED 120Hz, Snapdragon 8 Gen 3, камера Leica 50MP, батарея 4610mAh 90W", Decimal("39999"), 20),
            ("Xiaomi 14 12GB/512GB", "Флагман 2024. 6.36\" AMOLED 120Hz, Snapdragon 8 Gen 3, камера Leica 50MP, батарея 4610mAh 90W", Decimal("43999"), 18),
            ("Xiaomi 14 Pro 12GB/256GB", "Pro-флагман. 6.73\" AMOLED 120Hz, Snapdragon 8 Gen 3, камера Leica 50MP, батарея 4880mAh", Decimal("26635"), 15),
            ("Xiaomi 14 Pro 16GB/512GB", "Pro-флагман. 6.73\" AMOLED 120Hz, Snapdragon 8 Gen 3, камера Leica 50MP, батарея 4880mAh", Decimal("47999"), 12),
            ("Xiaomi 14 Ultra 12GB/512GB", "Топовий камерафон. 6.73\" AMOLED, Snapdragon 8 Gen 3, Leica 50MP квадро-камера", Decimal("54999"), 8),
            ("Xiaomi 14 Ultra 16GB/1TB", "Топовий камерафон. 6.73\" AMOLED, Snapdragon 8 Gen 3, Leica 50MP квадро-камера", Decimal("59999"), 6),

            # Xiaomi 13 Series
            ("Xiaomi 13 8GB/128GB", "Компактний флагман. 6.36\" AMOLED 120Hz, Snapdragon 8 Gen 2, камера Leica 50MP", Decimal("24999"), 25),
            ("Xiaomi 13 12GB/256GB", "Компактний флагман. 6.36\" AMOLED 120Hz, Snapdragon 8 Gen 2, камера Leica 50MP", Decimal("27999"), 20),
            ("Xiaomi 13 Pro 12GB/256GB", "Преміум камерафон. 6.73\" AMOLED, Snapdragon 8 Gen 2, Leica 50MP потрійна камера", Decimal("32999"), 15),

            # Redmi Note Series
            ("Redmi Note 13 Pro 8GB/256GB", "Середній клас. 6.67\" AMOLED 120Hz, Snapdragon 7s Gen 2, камера 200MP, батарея 5100mAh", Decimal("9300"), 50),
            ("Redmi Note 13 Pro 12GB/512GB", "Середній клас. 6.67\" AMOLED 120Hz, Snapdragon 7s Gen 2, камера 200MP, батарея 5100mAh", Decimal("11499"), 45),
            ("Redmi Note 13 6GB/128GB", "Бюджетний. 6.67\" AMOLED 120Hz, Snapdragon 685, камера 108MP, батарея 5000mAh", Decimal("6599"), 60),
            ("Redmi Note 12 Pro 8GB/256GB", "Популярна модель. 6.67\" AMOLED 120Hz, Dimensity 1080, камера 50MP, батарея 5000mAh 67W", Decimal("8999"), 40),
            ("Redmi Note 12 6GB/128GB", "Доступний. 6.67\" AMOLED 120Hz, Snapdragon 685, камера 48MP, батарея 5000mAh", Decimal("5999"), 55),

            # POCO Series
            ("POCO X6 Pro 8GB/256GB", "Ігровий середняк. 6.67\" AMOLED 120Hz, Dimensity 8300 Ultra, камера 64MP OIS, батарея 5000mAh", Decimal("12249"), 35),
            ("POCO X6 Pro 12GB/512GB", "Ігровий середняк. 6.67\" AMOLED 120Hz, Dimensity 8300 Ultra, камера 64MP OIS, батарея 5000mAh", Decimal("13940"), 30),
            ("POCO F5 8GB/256GB", "Флагманокілер. 6.67\" AMOLED 120Hz, Snapdragon 7+ Gen 2, камера 64MP, батарея 5000mAh", Decimal("11999"), 32),
            ("POCO M5 4GB/128GB", "Бюджетник. 6.58\" IPS 90Hz, Helio G99, камера 50MP, батарея 5000mAh", Decimal("4999"), 70),
            ("POCO C50 3GB/64GB", "Ультра-бюджет. 6.52\" IPS, MediaTek Helio A22, камера 8MP, батарея 5000mAh", Decimal("3199"), 80),

            # Vivo X200 Series
            ("Vivo X200 12GB/256GB", "Флагман 2024. 6.67\" AMOLED 120Hz, Dimensity 9400, камера ZEISS 50MP, батарея 5800mAh", Decimal("21564"), 18),
            ("Vivo X200 Pro 16GB/512GB", "Pro-камерафон. 6.78\" AMOLED 120Hz, Dimensity 9400, ZEISS камера 50MP телефото 200MP", Decimal("26280"), 12),
            ("Vivo X200 Pro Mini 12GB/256GB", "Компактний про. 6.31\" AMOLED 120Hz, Dimensity 9400, ZEISS 50MP потрійна камера", Decimal("23256"), 15),
            ("Vivo X200 Ultra 16GB/512GB", "Топ-камерафон. 6.78\" AMOLED, Dimensity 9400, ZEISS 1\" сенсор 50MP квадро-камера", Decimal("30999"), 8),
            ("Vivo X200 Ultra 16GB/1TB", "Топ-камерафон. 6.78\" AMOLED, Dimensity 9400, ZEISS 1\" сенсор 50MP квадро-камера", Decimal("51699"), 5),

            # Vivo X100 Series
            ("Vivo X100 12GB/256GB", "Флагман 2023. 6.78\" AMOLED 120Hz, Dimensity 9300, ZEISS камера 50MP", Decimal("24999"), 20),
            ("Vivo X100 Pro 16GB/512GB", "Камерафон. 6.78\" AMOLED 120Hz, Dimensity 9300, ZEISS 50MP потрійна камера APO телефото", Decimal("25482"), 15),

            # Vivo V Series
            ("Vivo V40 Pro 12GB/256GB", "Середній преміум. 6.78\" AMOLED 120Hz, Dimensity 9200+, ZEISS камера 50MP, батарея 5500mAh", Decimal("17424"), 30),
            ("Vivo V40 8GB/256GB", "Середній клас. 6.78\" AMOLED 120Hz, Snapdragon 7 Gen 3, камера 50MP, батарея 5500mAh", Decimal("13999"), 35),
            ("Vivo V30 8GB/256GB", "Стильний середняк. 6.78\" AMOLED 120Hz, Snapdragon 7 Gen 3, камера 50MP, батарея 5000mAh", Decimal("8399"), 40),
            ("Vivo V30 Pro 12GB/256GB", "Портретний камерафон. 6.78\" AMOLED 120Hz, Dimensity 8200, камера 50MP Aura Light", Decimal("15999"), 25),

            # Vivo iQOO Series
            ("Vivo iQOO 13 12GB/256GB", "Ігровий флагман. 6.82\" AMOLED 144Hz, Snapdragon 8 Elite, камера 50MP, батарея 6150mAh 120W", Decimal("20664"), 22),
            ("Vivo iQOO Z9 Turbo 12GB/256GB", "Ігровий середняк. 6.78\" AMOLED 144Hz, Snapdragon 8s Gen 3, камера 50MP, батарея 6000mAh", Decimal("9540"), 35),

            # Vivo Y Series
            ("Vivo Y200e 5G 8GB/128GB", "Доступний 5G. 6.67\" AMOLED 120Hz, Snapdragon 4 Gen 2, камера 50MP, батарея 5000mAh", Decimal("7999"), 45),
            ("Vivo Y19s 5G 6GB/128GB", "Бюджетний 5G. 6.68\" IPS 90Hz, Dimensity 6300, камера 50MP, батарея 5500mAh", Decimal("3960"), 60),

            # Google Pixel 9 Series
            ("Google Pixel 9 8GB/128GB", "Флагман 2024. 6.3\" OLED 120Hz, Tensor G4, камера 50MP, 7 років оновлень", Decimal("33333"), 20),
            ("Google Pixel 9 12GB/256GB", "Флагман 2024. 6.3\" OLED 120Hz, Tensor G4, камера 50MP, 7 років оновлень", Decimal("42499"), 15),
            ("Google Pixel 9 Pro 16GB/128GB", "Pro-серія. 6.3\" LTPO OLED 120Hz, Tensor G4, камера 50MP телефото 5x, AI функції", Decimal("35042"), 12),
            ("Google Pixel 9 Pro 16GB/256GB", "Pro-серія. 6.3\" LTPO OLED 120Hz, Tensor G4, камера 50MP телефото 5x, AI функції", Decimal("43999"), 10),
            ("Google Pixel 9 Pro XL 16GB/256GB", "Максимум Pixel. 6.8\" LTPO OLED 120Hz, Tensor G4, камера 50MP телефото 5x, батарея 5060mAh", Decimal("35999"), 8),
            ("Google Pixel 9 Pro XL 16GB/512GB", "Максимум Pixel. 6.8\" LTPO OLED 120Hz, Tensor G4, камера 50MP телефото 5x, батарея 5060mAh", Decimal("54999"), 6),
            ("Google Pixel 9 Pro Fold 16GB/256GB", "Складний флагман. 8\" Foldable OLED + 6.3\" зовнішній, Tensor G4, камера 48MP", Decimal("70149"), 5),

            # Google Pixel 8 Series
            ("Google Pixel 8 8GB/128GB", "Флагман 2023. 6.2\" OLED 120Hz, Tensor G3, камера 50MP, 7 років оновлень", Decimal("15252"), 30),
            ("Google Pixel 8 8GB/256GB", "Флагман 2023. 6.2\" OLED 120Hz, Tensor G3, камера 50MP, 7 років оновлень", Decimal("23099"), 25),
            ("Google Pixel 8 Pro 12GB/128GB", "Pro 2023. 6.7\" LTPO OLED 120Hz, Tensor G3, камера 50MP телефото 5x, Temperature sensor", Decimal("23999"), 18),
            ("Google Pixel 8 Pro 12GB/256GB", "Pro 2023. 6.7\" LTPO OLED 120Hz, Tensor G3, камера 50MP телефото 5x, Temperature sensor", Decimal("29999"), 15),
            ("Google Pixel 8a 8GB/128GB", "Доступний флагман. 6.1\" OLED 120Hz, Tensor G3, камера 64MP, 7 років оновлень", Decimal("13541"), 40),
            ("Google Pixel 8a 8GB/256GB", "Доступний флагман. 6.1\" OLED 120Hz, Tensor G3, камера 64MP, 7 років оновлень", Decimal("19020"), 35),

            # Google Pixel 7 Series
            ("Google Pixel 7 8GB/128GB", "Флагман 2022. 6.3\" AMOLED 90Hz, Tensor G2, камера 50MP, чистий Android", Decimal("22283"), 25),
            ("Google Pixel 7 Pro 12GB/128GB", "Pro 2022. 6.7\" LTPO OLED 120Hz, Tensor G2, камера 50MP телефото 5x", Decimal("25819"), 18),
            ("Google Pixel 7 Pro 12GB/256GB", "Pro 2022. 6.7\" LTPO OLED 120Hz, Tensor G2, камера 50MP телефото 5x", Decimal("28999"), 15),
            ("Google Pixel 7a 8GB/128GB", "Середній клас. 6.1\" OLED 90Hz, Tensor G2, камера 64MP, швидка зарядка 18W", Decimal("16680"), 35),

            # Google Pixel Fold
            ("Google Pixel Fold 12GB/256GB", "Перший Pixel Fold. 7.6\" Foldable OLED + 5.8\" зовнішній, Tensor G2, камера 48MP", Decimal("34799"), 6),
            ("Google Pixel Fold 12GB/512GB", "Перший Pixel Fold. 7.6\" Foldable OLED + 5.8\" зовнішній, Tensor G2, камера 48MP", Decimal("52006"), 4),
        ]

        products_created = 0
        for name, description, price, stock in phones:
            Product.objects.create(
                category=phone_category,
                name=name,
                description=description,
                price=price,
                stock=stock,
            )
            products_created += 1

        price_stats = Product.objects.aggregate(
            min_price=models.Min('price'),
            max_price=models.Max('price')
        )

        # ===================== APPLY RANDOM DISCOUNTS =====================
        self.stdout.write("Applying random discounts to 50% of products...")
        
        all_products = list(Product.objects.all())
        # Select random half of products for discounts
        discount_count = len(all_products) // 2
        products_to_discount = random.sample(all_products, discount_count)
        
        for product in products_to_discount:
            # Random discount between 10-20%
            discount_percent = random.randint(10, 20)
            sale_price = product.price * (Decimal('1') - Decimal(discount_percent) / Decimal('100'))
            product.sale_price = sale_price.quantize(Decimal('0.01'))
            product.save()
        
        discount_stats = Product.objects.filter(sale_price__isnull=False).aggregate(
            count=models.Count('id'),
            avg_discount=models.Avg(
                models.F('price') - models.F('sale_price')
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Database seeded successfully!\n"
                f"  - Phone Category: {phone_category.name}\n"
                f"  - Total Products: {Product.objects.count()} mobile phones\n"
                f"  - Products with discounts: {discount_stats['count']} ({discount_stats['count']/Product.objects.count()*100:.1f}%)\n"
                f"  - Price Range: {price_stats['min_price']} - {price_stats['max_price']} UAH\n"
                f"  - All prices in UAH"
            )
        )
