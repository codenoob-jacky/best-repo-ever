from django import template

register = template.Library()

@register.filter
def split(value, delimiter='|'):
    """
    Splits the value by the delimiter and returns a list
    Usage: {{ value|split:',' }}
    """
    return value.split(delimiter)