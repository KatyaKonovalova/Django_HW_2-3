import json
from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('category.json', 'r') as f:
            raw_data = json.load(f.read())
            return raw_data

    # Здесь мы получаем данные из фикстур с категориями

    @staticmethod
    def json_read_products():
        with open('products.json', 'r') as f:
            raw_data = json.load(f.read())
            return raw_data

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):

        with connection.cursor() as cursor:

            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1")

            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1")

        Product.objects.all().delete()
        Category.objects.all().delete()

        # Удалите все продукты
        # Удалите все категории

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(**category.get('fields', {}))
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(category=Category.objects.get(pk=category_pk), **product.get('fields', {}))
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
