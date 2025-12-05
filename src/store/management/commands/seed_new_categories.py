from django.core.management.base import BaseCommand
from store.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Seeds new categories and products'

    def handle(self, *args, **kwargs):
        categories_data = [
            {
                'name': 'Навушники',
                'slug': 'headphones',
                'products': [
                    ('Apple AirPods Pro', 8999), ('Samsung Galaxy Buds2', 3999), ('Sony WH-1000XM5', 12999),
                    ('JBL Tune 510BT', 1699), ('Marshall Major IV', 5499), ('Xiaomi Redmi Buds 4', 999),
                    ('Sennheiser Momentum 4', 14999), ('Bose QuietComfort 45', 11999), ('Huawei FreeBuds 5i', 2499),
                    ('Beats Studio3', 9999), ('Anker Soundcore Life Q30', 2999), ('Philips TAT2206', 1199),
                    ('Panasonic RZ-S500W', 3499), ('Realme Buds Air 3', 1999), ('OPPO Enco Air2', 1499),
                    ('Logitech G435', 2999), ('Razer Barracuda X', 3999), ('SteelSeries Arctis Nova 1', 2499),
                    ('HyperX Cloud II', 3499), ('Asus ROG Cetra', 3999), ('Koss Porta Pro', 1999),
                    ('Beyerdynamic DT 770 Pro', 6499), ('Audio-Technica ATH-M50x', 6999), ('AKG K371', 5499),
                    ('Shure SE215', 4999), ('FiiO FH3', 5999), ('Moondrop Aria', 3499), ('KZ ZS10 Pro', 1499),
                    ('SoundPEATS Air3', 1999), ('Edifier W820NB', 2499)
                ]
            },
            {
                'name': 'Планшети',
                'slug': 'tablets',
                'products': [
                    ('Apple iPad 10.2', 14999), ('Samsung Galaxy Tab S8', 29999), ('Xiaomi Pad 6', 15999),
                    ('Lenovo Tab P11', 9999), ('Realme Pad', 7999), ('Huawei MatePad 11', 13999),
                    ('Microsoft Surface Go 3', 19999), ('Blackview Tab 15', 6999), ('Teclast T40 Pro', 7499),
                    ('Oukitel RT2', 11999), ('Apple iPad Air', 26999), ('Samsung Galaxy Tab A8', 7999),
                    ('Lenovo Yoga Tab 13', 24999), ('Xiaomi Redmi Pad', 8999), ('Nokia T21', 9499),
                    ('Amazon Fire HD 10', 4999), ('TCL Tab 10s', 5999), ('Prestigio MultiPad', 3999),
                    ('Pixus Joker', 4499), ('Sigma mobile X-style', 3499), ('Apple iPad Pro 11', 38999),
                    ('Samsung Galaxy Tab S9', 34999), ('Lenovo Tab M10', 5999), ('Huawei MatePad SE', 6499),
                    ('Realme Pad Mini', 5499), ('Chuwi HiPad Max', 8999), ('Cubot Tab 30', 5999),
                    ('Doogee T10', 6999), ('Ulefone Tab A7', 4999), ('ZTE Blade X10', 4499)
                ]
            },
            {
                'name': 'Смарт-годинники',
                'slug': 'smartwatches',
                'products': [
                    ('Apple Watch Series 8', 18999), ('Samsung Galaxy Watch5', 9999), ('Garmin Fenix 7', 34999),
                    ('Xiaomi Watch S1', 6999), ('Amazfit GTR 4', 7499), ('Huawei Watch GT 3', 8999),
                    ('Fitbit Versa 4', 8499), ('Suunto 9 Peak', 19999), ('Polar Vantage V2', 21999),
                    ('Casio G-Shock Smart', 14999), ('Apple Watch SE', 11999), ('Samsung Galaxy Watch4', 6999),
                    ('Garmin Venu 2', 16999), ('Xiaomi Smart Band 7 Pro', 2999), ('Amazfit GTS 4', 7499),
                    ('Huawei Watch Fit 2', 4999), ('Realme Watch 3', 2499), ('OPPO Watch Free', 2999),
                    ('Mobvoi TicWatch Pro 3', 11999), ('Fossil Gen 6', 10999), ('Withings ScanWatch', 12999),
                    ('Zepp E Circle', 5499), ('Haylou RS4 Plus', 1999), ('Mibro Watch X1', 1499),
                    ('Kospet Tank M1', 1999), ('Zeblaze Stratos 2', 2499), ('North Edge Apache', 2999),
                    ('Skmei Smart', 999), ('Canyon Wasabi', 1499), ('Gelius Pro', 1299)
                ]
            },
            {
                'name': 'Ноутбуки',
                'slug': 'laptops',
                'products': [
                    ('Apple MacBook Air M1', 39999), ('Asus ROG Strix G15', 49999), ('Lenovo Legion 5', 44999),
                    ('HP Pavilion 15', 24999), ('Dell XPS 13', 59999), ('Acer Nitro 5', 34999),
                    ('MSI Katana GF66', 39999), ('Apple MacBook Pro 14', 79999), ('Asus ZenBook 14', 39999),
                    ('Lenovo IdeaPad 3', 19999), ('HP Omen 16', 54999), ('Dell G15', 39999),
                    ('Acer Swift 3', 29999), ('MSI Modern 14', 24999), ('Gigabyte G5', 34999),
                    ('Razer Blade 15', 99999), ('Alienware x15', 89999), ('Microsoft Surface Laptop 5', 49999),
                    ('Huawei MateBook D15', 24999), ('Xiaomi RedmiBook Pro', 34999), ('Realme Book', 29999),
                    ('Samsung Galaxy Book2', 39999), ('LG Gram 17', 69999), ('Fujitsu Lifebook', 44999),
                    ('Panasonic Toughbook', 99999), ('Dream Machines RG3060', 44999), ('XMG Neo 15', 79999),
                    ('Schenker XMG', 69999), ('Chuwi GemiBook', 14999), ('Teclast F15 Plus', 12999)
                ]
            },
            {
                'name': 'Аксесуари',
                'slug': 'accessories',
                'products': [
                    ('Чохол для iPhone 14', 499), ('Захисне скло Samsung S23', 299), ('Кабель USB-C Baseus', 199),
                    ('Зарядний пристрій Apple 20W', 999), ('PowerBank Xiaomi 20000mAh', 1499), ('Мишка Logitech G102', 999),
                    ('Клавіатура Keychron K2', 3999), ('Підставка для ноутбука', 799), ('Сумка для ноутбука 15.6"', 899),
                    ('HDMI кабель 2м', 299), ('Перехідник USB-C Hub', 1499), ('Карта пам\'яті Kingston 64GB', 399),
                    ('Флешка SanDisk 128GB', 599), ('Веб-камера Logitech C920', 2999), ('Мікрофон HyperX QuadCast', 5999),
                    ('Килимок для миші SteelSeries', 499), ('Тримач для телефону в авто', 399), ('Селфі-палиця Xiaomi', 499),
                    ('Кільцева лампа', 899), ('Штатив для камери', 1499), ('Рюкзак для ноутбука HP', 1299),
                    ('Охолоджуюча підставка', 699), ('Зовнішній HDD WD 1TB', 2499), ('Зовнішній SSD Samsung T7', 3999),
                    ('Мережевий фільтр Xiaomi', 599), ('Батарейки Duracell AA', 199), ('Акумулятори Panasonic Eneloop', 799),
                    ('Зарядний пристрій для батарейок', 499), ('Органайзер для кабелів', 149), ('Спрей для екрану', 99)
                ]
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category exists: {category.name}')

            for prod_name, price in cat_data['products']:
                # Add some randomness to price and stock
                final_price = price
                stock = random.randint(5, 100)
                
                # Check if product exists to avoid duplicates
                if not Product.objects.filter(name=prod_name, category=category).exists():
                    Product.objects.create(
                        category=category,
                        name=prod_name,
                        description=f"Опис для {prod_name}. Чудовий вибір для вас!",
                        price=final_price,
                        stock=stock
                    )
                    self.stdout.write(f'  Created product: {prod_name}')
                else:
                    self.stdout.write(f'  Product exists: {prod_name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded new categories and products'))
