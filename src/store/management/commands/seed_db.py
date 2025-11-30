from decimal import Decimal
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from store.models import Category, Product


class Command(BaseCommand):
    help = "Seeds the database with initial data (users, categories, products in UAH)"

    def handle(self, *args, **kwargs):
        fake = Faker("ru_RU")

        # Если товары уже есть — ничего не делаем (чтобы не плодить дубли)
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Products already exist, skipping seeding."
            ))
            return

        self.stdout.write(self.style.WARNING("Seeding database..."))

        # ===================== USERS =====================
        self.stdout.write("Creating users...")
        users_created = 0
        for _ in range(10):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password="password123",
                )
                users_created += 1
        self.stdout.write(f"Created {users_created} regular users")

        # Superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin/admin"))

        # ===================== CATEGORIES =====================
        self.stdout.write("Creating categories...")

        category_data = {
            "Электроника": {
                "slug": "electronics",
                "products": [
                    "Смартфон",
                    "Планшет",
                    "Умные часы",
                    "Фитнес-браслет",
                    "Электронная книга",
                    "Портативная колонка",
                    "Наушники",
                    "Bluetooth-гарнитура",
                    "Power Bank",
                    "Солнечная панель",
                    "Умная лампочка",
                    "Робот-пылесос",
                    "Умный термостат",
                    "IP-камера",
                    "Умный замок",
                    "Электронный замок",
                    "Умный выключатель",
                    "Wi-Fi роутер",
                    "Сетевой фильтр",
                    "USB-хаб",
                ],
            },
            "Компьютеры": {
                "slug": "computers",
                "products": [
                    "Ноутбук",
                    "Игровой ПК",
                    "Монитор",
                    "Клавиатура",
                    "Компьютерная мышь",
                    "Веб-камера",
                    "Микрофон",
                    "Колонки для ПК",
                    "SSD накопитель",
                    "Оперативная память",
                    "Видеокарта",
                    "Процессор",
                    "Материнская плата",
                    "Блок питания",
                    "Корпус для ПК",
                    "Кулер для процессора",
                    "Термопаста",
                    "Коврик для мыши",
                    "Подставка для ноутбука",
                    "USB-флешка",
                ],
            },
            "Смартфоны": {
                "slug": "smartphones",
                "products": [
                    "iPhone",
                    "Samsung Galaxy",
                    "Xiaomi",
                    "Huawei",
                    "OnePlus",
                    "Google Pixel",
                    "Sony Xperia",
                    "Nokia",
                    "Motorola",
                    "Realme",
                    "Oppo",
                    "Vivo",
                    "Honor",
                    "Poco",
                    "Redmi",
                    "Meizu",
                    "Asus Zenfone",
                    "LG",
                    "BlackBerry",
                    "ZTE",
                ],
            },
            "Аксессуары": {
                "slug": "accessories",
                "products": [
                    "Чехол для телефона",
                    "Защитное стекло",
                    "Карта памяти",
                    "Зарядное устройство",
                    "Кабель USB-C",
                    "Кабель Lightning",
                    "Автомобильное зарядное",
                    "Держатель для телефона",
                    "Селфи-палка",
                    "Стабилизатор для камеры",
                    "Внешний аккумулятор",
                    "Беспроводная зарядка",
                    "Адаптер USB-C",
                    "Разветвитель для наушников",
                    "Чистящие салфетки",
                    "Стилус",
                    "Кольцо-держатель",
                    "Поп-сокет",
                    "Магнитный держатель",
                    "Подставка для телефона",
                ],
            },
            "Игровые устройства": {
                "slug": "gaming",
                "products": [
                    "Игровая консоль",
                    "Игровой контроллер",
                    "Игровая клавиатура",
                    "Игровая мышь",
                    "Игровой коврик",
                    "Игровые наушники",
                    "Игровой микрофон",
                    "Игровой монитор",
                    "Игровое кресло",
                    "Игровой стол",
                    "Игровая гарнитура VR",
                    "Рулевое колесо",
                    "Джойстик",
                    "Геймпад",
                    "Игровая приставка",
                    "Игровая подставка",
                    "Игровой коврик расширенный",
                    "Игровая мышь беспроводная",
                    "Игровая клавиатура механическая",
                    "Игровой монитор 4K",
                    "Игровая веб-камера",
                ],
            },
        }

        category_objs = []
        for cat_name, data in category_data.items():
            cat, created = Category.objects.get_or_create(
                slug=data["slug"],
                defaults={"name": cat_name},
            )
            if created:
                self.stdout.write(f"  Created category: {cat_name}")
            category_objs.append(cat)

        # ===================== PRODUCTS =====================
        self.stdout.write("Creating products (prices in UAH)...")

        PRICE_RANGES = {
            "Смартфоны": (Decimal("3000"), Decimal("60000")),
            "Компьютеры": (Decimal("8000"), Decimal("80000")),
            "Игровые устройства": (Decimal("1500"), Decimal("40000")),
            "DEFAULT": (Decimal("300"), Decimal("20000")),
        }

        products_created = 0

        for category_obj in category_objs:
            category_name = category_obj.name
            product_names = category_data[category_name]["products"]

            products_per_category = 20  # всего выйдет около 100 товаров

            for _ in range(products_per_category):
                base_name = random.choice(product_names)

                variations = [
                    f"{base_name} {fake.word().capitalize()}",
                    f"{base_name} {random.choice(['Pro', 'Max', 'Plus', 'Mini', 'Ultra', 'Premium', 'Standard'])}",
                    f"{base_name} {fake.company_suffix()}",
                    f"{base_name} {random.randint(1, 20)}",
                ]
                product_name = random.choice(variations)

                description = fake.text(max_nb_chars=200)

                min_price, max_price = PRICE_RANGES.get(
                    category_name,
                    PRICE_RANGES["DEFAULT"],
                )

                raw_price = random.randint(
                    int(min_price * 100),
                    int(max_price * 100),
                )
                price = Decimal(raw_price) / Decimal("100")

                Product.objects.create(
                    category=category_obj,
                    name=product_name,
                    description=description,
                    price=price,
                    stock=random.randint(0, 150),
                )
                products_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Database seeded successfully!\n"
                f"  - Users (non-super): {User.objects.filter(is_superuser=False).count()}\n"
                f"  - Categories: {Category.objects.count()}\n"
                f"  - Products: {Product.objects.count()} (all prices in UAH)"
            )
        )
