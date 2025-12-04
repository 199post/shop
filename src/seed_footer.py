import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import FooterSection, FooterLink, Page

def seed_footer():
    print("Seeding footer...")
    
    # Clear existing
    FooterSection.objects.all().delete()
    Page.objects.all().delete()

    # Sections
    sections_data = [
        {
            "title": "Інформація про компанію",
            "order": 1,
            "links": [
                {"title": "Про нас", "url": "/page/about-us/"},
                {"title": "Умови використання сайту", "url": "/page/terms/"},
                {"title": "Вакансії", "url": "/page/jobs/"},
                {"title": "Контакти", "url": "/page/contacts/"},
            ]
        },
        {
            "title": "Допомога",
            "order": 2,
            "links": [
                {"title": "Доставка та оплата", "url": "/page/delivery/"},
                {"title": "Кредит", "url": "/page/credit/"},
                {"title": "Гарантія", "url": "/page/warranty/"},
                {"title": "Повернення товару", "url": "/page/returns/"},
                {"title": "Сервісні центри", "url": "/page/service/"},
            ]
        },
        {
            "title": "Сервіси",
            "order": 3,
            "links": [
                {"title": "Бонусний рахунок", "url": "/page/bonus/"},
                {"title": "Nice-Price Обмін", "url": "/page/exchange/"},
                {"title": "Подарункові сертифікати", "url": "/page/gift-cards/"},
            ]
        },
        {
            "title": "Партнерам",
            "order": 4,
            "links": [
                {"title": "Продавати на Nice-Price", "url": "/page/sell/"},
                {"title": "Співпраця з нами", "url": "/page/cooperation/"},
                {"title": "Франчайзинг", "url": "/page/franchise/"},
                {"title": "Оренда приміщень", "url": "/page/rent/"},
            ]
        }
    ]

    for sec_data in sections_data:
        section = FooterSection.objects.create(title=sec_data['title'], order=sec_data['order'])
        for i, link_data in enumerate(sec_data['links']):
            FooterLink.objects.create(
                section=section,
                title=link_data['title'],
                url=link_data['url'],
                order=i+1
            )
            
            # Create a dummy page for each link if it looks like a page
            if link_data['url'].startswith('/page/'):
                slug = link_data['url'].split('/')[-2]
                Page.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': link_data['title'],
                        'content': f"<h1>{link_data['title']}</h1><p>Тут буде інформація про {link_data['title'].lower()}.</p>"
                    }
                )

    print("Footer seeded successfully!")

if __name__ == '__main__':
    seed_footer()
