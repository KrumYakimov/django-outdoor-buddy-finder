from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def slugify(value):
    return slugify(value)
