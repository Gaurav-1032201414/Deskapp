from django import template

register = template.Library()

@register.filter(name='lower_and_endswith')
def lower_and_endswith(value, endswith):
    return value.lower().endswith(endswith)