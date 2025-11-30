from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        fake = Faker()

        # Create Users
        self.stdout.write('Creating users...')
        for _ in range(10):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123'
                )

        # Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser: admin/admin')

        # Create Categories
        self.stdout.write('Creating categories...')
        categories = ['Electronics', 'Computers', 'Smartphones', 'Accessories', 'Gaming']
        category_objs = []
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': fake.slug()}
            )
            category_objs.append(cat)

        # Create Products
        self.stdout.write('Creating products...')
        for _ in range(100):
            Product.objects.create(
                category=random.choice(category_objs),
                name=fake.catch_phrase(),
                description=fake.text(),
                price=round(random.uniform(10.0, 1000.0), 2),
                stock=random.randint(0, 100)
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
