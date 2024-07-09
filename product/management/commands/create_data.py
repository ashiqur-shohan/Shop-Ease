import requests
from django.core.management import BaseCommand
from django.utils.text import slugify
from product.models import Product,Category

# ref - https://www.youtube.com/watch?v=kT9Liv1biAE&list=PLoomN1iY7V9lGJn34sqBgRj2lAuCOYKbs&index=4
# from 10 min 

class Command(BaseCommand):
    def handle(self, *args, **options) :
        response = requests.get('https://fakestoreapi.com/products').json()
        for product in response:
            category , _ = Category.objects.get_or_create(
                title = product['category'],
                slug=slugify(product['category']),
                featured = True
            )
            Product.objects.create(
                category = category,
                title = product['title'],
                slug=slugify(product['title']),
                price = product['price'],
                thumbnail=product['image'],
                description=product['description']
            )

