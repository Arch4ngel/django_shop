import json

from django.core.management import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        category_fill = []
        with open('catalog_data.json', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if item["model"] == "catalog.category":
                    category_fill.append(
                        Category(**item['fields']))
        Category.objects.bulk_create(category_fill)
