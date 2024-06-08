# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='pprint')
def pprint(value):
    from pprint import pformat
    return pformat(value)
