from config import settings
from django.core.cache import cache
from catalog.models import Category


def cache_category(category_pk):
    if settings.CACHE_ENABLED:
        key = f'category_list{category_pk}'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.filter(category_pk=category_pk)
            cache.set(key, category_list)
    else:
        category_list = Category.objects.filter(category_pk=category_pk)

    return category_list
