from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
import os


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open(os.path.join(os.path.dirname(__file__), 'catalog_data.json')) as f:
            data = json.load(f)

        # Фильтруем данные, оставляя только словари с моделью "catalog.category"
        categories_data = [category for category in data if category["model"] == "catalog.category"]

        # Преобразуем данные в список словарей с информацией о категориях
        categories = [{"name": category["fields"]["name"], "description": category["fields"]["description"]} for
                      category in categories_data]

        return categories

    @staticmethod
    def json_read_products():
        with open(os.path.join(os.path.dirname(__file__), 'catalog_data.json')) as f:
            data = json.load(f)

        # Фильтруем данные, оставляя только словари с моделью "catalog.product"
        products_data = [product for product in data if product["model"] == "catalog.product"]

        # Преобразуем данные в список словарей с информацией о продуктах
        products = [{"name": product["fields"]["name"], "description": product["fields"]["description"],
                     "image": product["fields"]["image"], "price": product["fields"]["price"],
                     "category": product["fields"]["category"]} for product in products_data]

        return products

    def handle(self, *args, **options):

        # Удаление всех продуктов
        Product.objects.all().delete()

        # Удаление всех категорий
        Category.objects.all().delete()

        # Создание списков для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(name=category['name'], description=category['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read_products():
            try:
                category = Category.objects.get(
                    name=product['category'])  # Получаем категорию из базы данных для корректной связки объектов
            except Category.DoesNotExist:
                # Если категория не найдена, пропускаем текущий продукт
                print(f"Category '{product['category']}' Не найдена. Пропуск продукта '{product['name']}'.")
                continue
            product_for_create.append(
                Product(name=product['name'], description=product['description'], image=product['image'],
                        price=product['price'], category=category)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Успешная загрузка данных из JSON файла в БД.'))
