from django import template

register = template.Library()

@register.filter(name='gender')
def gender(value):
    """..."""
    return "hest"

