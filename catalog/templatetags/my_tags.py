import datetime
from django import template
from catalog.models import Category

register = template.Library()


# Создание тега
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
@register.filter(needs_autoescape=True)
def mediapath(path):
    if path:
        return f'media/{path}'


@register.simple_tag
def category_list():
    return Category.objects.all()
